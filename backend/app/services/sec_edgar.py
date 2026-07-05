"""Live fetcher for SEC EDGAR Form 4 (insider transaction) filings.
No API key is required, but SEC requires a descriptive User-Agent header
on every request (see SEC_USER_AGENT in config) and asks that requests
stay under ~10/sec.

Flow:
1. GET the "getcurrent" Atom feed for type=4 filings -- this lists the
   most recently filed Form 4s network-wide, newest first.
2. For each entry, derive the CIK + accession number from the entry's
   index-page link, then fetch that filing's primary_doc.xml (the
   standard machine-readable ownership document EDGAR generates for
   every electronically-filed Form 4 since the paper-filing era ended).
3. Parse the ownership XML for the issuer ticker/name, the reporting
   owner's name/title, and each non-derivative (open-market) buy/sell
   transaction.

Only transaction codes "P" (open-market purchase) and "S" (open-market
sale) are kept -- grants, option exercises, gifts, etc. aren't a candid
buy/sell signal and are filtered out.
"""

import asyncio
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import httpx

from app.config import settings
from app.services.sample_data import SAMPLE_INSIDER_FILINGS

logger = logging.getLogger(__name__)

FEED_URL = "https://www.sec.gov/cgi-bin/browse-edgar"
ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}
MAX_FILINGS = 25
REQUEST_DELAY_SECONDS = 0.15


def _text(el: ET.Element | None) -> str | None:
    if el is None or el.text is None:
        return None
    return el.text.strip()


async def _fetch_feed_entries(client: httpx.AsyncClient) -> list[dict]:
    params = {
        "action": "getcurrent",
        "type": "4",
        "company": "",
        "dateb": "",
        "owner": "include",
        "count": "100",
        "output": "atom",
    }
    resp = await client.get(FEED_URL, params=params)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)

    entries = []
    for entry in root.findall("a:entry", ATOM_NS):
        link_el = entry.find("a:link", ATOM_NS)
        href = link_el.get("href") if link_el is not None else None
        if not href:
            continue
        match = re.search(r"/data/(\d+)/(\d+)-index", href)
        if not match:
            continue
        cik, accession_nodashes = match.groups()
        entries.append(dict(cik=cik, accession_nodashes=accession_nodashes,
                             filing_date=_text(entry.find("a:updated", ATOM_NS))))
    return entries


async def _fetch_filing_detail(client: httpx.AsyncClient, cik: str, accession_nodashes: str) -> list[dict]:
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nodashes}/primary_doc.xml"
    resp = await client.get(url)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)

    ticker = _text(root.find(".//issuerTradingSymbol"))
    company = _text(root.find(".//issuerName"))
    insider_name = _text(root.find(".//rptOwnerName"))
    is_officer = _text(root.find(".//isOfficer"))
    role = _text(root.find(".//officerTitle")) or ("Director" if _text(root.find(".//isDirector")) == "1" else None)
    period = _text(root.find(".//periodOfReport"))

    if not ticker or not company or not insider_name:
        return []

    results = []
    for tx in root.findall(".//nonDerivativeTable/nonDerivativeTransaction"):
        code = _text(tx.find(".//transactionCoding/transactionCode"))
        if code not in ("P", "S"):
            continue
        shares_text = _text(tx.find(".//transactionAmounts/transactionShares/value"))
        price_text = _text(tx.find(".//transactionAmounts/transactionPricePerShare/value"))
        tx_date = _text(tx.find(".//transactionDate/value")) or period
        try:
            shares = float(shares_text) if shares_text else None
            price = float(price_text) if price_text else None
        except ValueError:
            shares = price = None
        value = round(shares * price, 2) if shares is not None and price is not None else None

        results.append(dict(
            id=f"sec-{accession_nodashes}-{len(results)}",
            ticker=ticker.upper(),
            company=company,
            insider_name=insider_name,
            role=role or ("Officer" if is_officer == "1" else "Insider"),
            transaction_type="buy" if code == "P" else "sell",
            shares=shares,
            price_per_share=price,
            value=value,
            filing_date=period or tx_date,
            transaction_date=tx_date,
            source_url=f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nodashes}/",
        ))
    return results


async def _fetch_live() -> list[dict]:
    headers = {"User-Agent": settings.sec_user_agent}
    async with httpx.AsyncClient(timeout=15, headers=headers) as client:
        entries = await _fetch_feed_entries(client)
        entries = entries[:MAX_FILINGS]

        filings: list[dict] = []
        for e in entries:
            try:
                filings.extend(await _fetch_filing_detail(client, e["cik"], e["accession_nodashes"]))
            except Exception as ex:
                logger.warning("Skipping unparsable Form 4 filing %s: %s", e, ex)
            await asyncio.sleep(REQUEST_DELAY_SECONDS)

    if not filings:
        raise ValueError("SEC EDGAR returned no usable Form 4 filings")

    now = datetime.now(timezone.utc)
    for f in filings:
        f["is_sample"] = False
        f["fetched_at"] = now
    return filings


async def fetch_insider_filings() -> tuple[list[dict], bool]:
    """Returns (filings, is_sample_fallback)."""
    try:
        return await _fetch_live(), False
    except Exception as e:
        logger.warning("SEC EDGAR live fetch failed, using sample data: %s", e)
        now = datetime.now(timezone.utc)
        sample = [dict(f, is_sample=True, fetched_at=now) for f in SAMPLE_INSIDER_FILINGS]
        return sample, True
