"""Live fetcher for congressional stock trade disclosures.

Uses the well-known public JSON dumps published by the House Stock Watcher
and Senate Stock Watcher projects, which scrape and structure the official
(but PDF/text) Periodic Transaction Reports members of Congress are legally
required to file. No API key required. These trades are disclosed on a
legal delay of up to ~45 days after the transaction date.
"""

import logging
import re
from datetime import datetime, timezone

import httpx

from app.services.sample_data import SAMPLE_CONGRESS_TRADES
from app.services.ticker_map import company_name

logger = logging.getLogger(__name__)

HOUSE_URL = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
SENATE_URL = "https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.json"

MAX_PER_CHAMBER = 150
TICKER_RE = re.compile(r"^[A-Z]{1,5}$")


def _to_iso_date(value: str | None) -> str | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return value


def _transaction_type(raw: str | None) -> str | None:
    if not raw:
        return None
    lowered = raw.lower()
    if "purchase" in lowered:
        return "buy"
    if "sale" in lowered:
        return "sell"
    if "exchange" in lowered:
        return "exchange"
    return None


def _amount_range(raw: str | None) -> tuple[str, float | None, float | None]:
    if not raw:
        return "Unknown", None, None
    numbers = [float(n.replace(",", "")) for n in re.findall(r"[\d,]+(?:\.\d+)?", raw)]
    if len(numbers) >= 2:
        return raw, numbers[0], numbers[1]
    if len(numbers) == 1:
        return raw, numbers[0], numbers[0]
    return raw, None, None


def _clean_name(raw: str | None) -> str | None:
    if not raw:
        return None
    return re.sub(r"^(Hon\.|Sen\.|Rep\.)\s+", "", raw).strip()


def _parse_entries(raw_entries: list[dict], chamber: str) -> list[dict]:
    now = datetime.now(timezone.utc)
    out = []
    for e in raw_entries:
        ticker = (e.get("ticker") or "").strip().upper()
        if not ticker or not TICKER_RE.match(ticker) or ticker in ("N/A", "--"):
            continue
        tx_type = _transaction_type(e.get("type"))
        if tx_type is None:
            continue
        name = _clean_name(e.get("representative") or e.get("senator"))
        if not name:
            continue
        amount_range, amount_min, amount_max = _amount_range(e.get("amount"))
        tx_date = _to_iso_date(e.get("transaction_date"))
        disc_date = _to_iso_date(e.get("disclosure_date"))
        if not tx_date or not disc_date:
            continue

        out.append(dict(
            id=f"{chamber}-{ticker}-{tx_date}-{name}-{len(out)}",
            representative=name,
            chamber=chamber,
            party=e.get("party"),
            ticker=ticker,
            company=company_name(ticker, e.get("asset_description", "")),
            transaction_type=tx_type,
            amount_range=amount_range,
            amount_min=amount_min,
            amount_max=amount_max,
            transaction_date=tx_date,
            disclosure_date=disc_date,
            is_sample=False,
            fetched_at=now,
        ))
    out.sort(key=lambda t: t["disclosure_date"], reverse=True)
    return out[:MAX_PER_CHAMBER]


async def _fetch_live() -> list[dict]:
    async with httpx.AsyncClient(timeout=20) as client:
        house_resp, senate_resp = await client.get(HOUSE_URL), await client.get(SENATE_URL)
        house_resp.raise_for_status()
        senate_resp.raise_for_status()

    trades = _parse_entries(house_resp.json(), "house") + _parse_entries(senate_resp.json(), "senate")
    if not trades:
        raise ValueError("Congressional trade sources returned no usable data")
    return trades


async def fetch_congress_trades() -> tuple[list[dict], bool]:
    """Returns (trades, is_sample_fallback)."""
    try:
        return await _fetch_live(), False
    except Exception as e:
        logger.warning("Congress trade live fetch failed, using sample data: %s", e)
        now = datetime.now(timezone.utc)
        sample = [dict(t, is_sample=True, fetched_at=now) for t in SAMPLE_CONGRESS_TRADES]
        return sample, True
