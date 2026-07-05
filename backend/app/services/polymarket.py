"""Live fetcher for Polymarket's public Gamma API (no key required).
Docs: https://docs.polymarket.com/ -- GET /markets returns active markets
with outcomes/outcomePrices as JSON-encoded string arrays.
"""

import json
import logging
from datetime import datetime, timezone

import httpx

from app.services.sample_data import SAMPLE_POLYMARKET_MARKETS
from app.services.ticker_map import match_tickers

logger = logging.getLogger(__name__)

GAMMA_MARKETS_URL = "https://gamma-api.polymarket.com/markets"


async def _fetch_live() -> list[dict]:
    params = {
        "active": "true",
        "closed": "false",
        "order": "volume24hr",
        "ascending": "false",
        "limit": 40,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(GAMMA_MARKETS_URL, params=params)
        resp.raise_for_status()
        raw_markets = resp.json()

    now = datetime.now(timezone.utc)
    markets: list[dict] = []
    for m in raw_markets:
        try:
            outcomes = json.loads(m.get("outcomes", "[]") or "[]")
            prices = json.loads(m.get("outcomePrices", "[]") or "[]")
            if len(prices) < 2 or len(outcomes) < 2:
                continue
            yes_price = float(prices[0])
            no_price = float(prices[1])
            question = m.get("question", "").strip()
            if not question:
                continue

            price_change = m.get("oneDayPriceChange")
            change_24h = float(price_change) * 100 if price_change is not None else None

            markets.append(dict(
                id=str(m.get("id") or m.get("slug") or question),
                question=question,
                category=(m.get("category") or None),
                yes_price=round(yes_price, 4),
                no_price=round(no_price, 4),
                change_24h=round(change_24h, 2) if change_24h is not None else None,
                volume=float(m.get("volume") or 0),
                liquidity=float(m.get("liquidity") or 0),
                end_date=m.get("endDate"),
                tickers=match_tickers(question),
                url=f"https://polymarket.com/event/{m.get('slug')}" if m.get("slug") else None,
                is_sample=False,
                fetched_at=now,
            ))
        except (ValueError, TypeError, KeyError) as e:
            logger.warning("Skipping malformed Polymarket market: %s", e)
            continue

    if not markets:
        raise ValueError("Polymarket returned no usable markets")
    return markets


async def fetch_polymarket_markets() -> tuple[list[dict], bool]:
    """Returns (markets, is_sample_fallback)."""
    try:
        return await _fetch_live(), False
    except Exception as e:
        logger.warning("Polymarket live fetch failed, using sample data: %s", e)
        now = datetime.now(timezone.utc)
        sample = [dict(m, is_sample=True, fetched_at=now) for m in SAMPLE_POLYMARKET_MARKETS]
        return sample, True
