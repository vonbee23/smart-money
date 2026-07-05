import logging
from datetime import datetime, timezone

from app.db import congress_collection, insiders_collection, meta_collection, polymarket_collection
from app.services.congress import fetch_congress_trades
from app.services.polymarket import fetch_polymarket_markets
from app.services.sec_edgar import fetch_insider_filings

logger = logging.getLogger(__name__)


async def _replace_collection(collection, records: list[dict]) -> None:
    await collection.delete_many({})
    if records:
        await collection.insert_many(records)


async def _set_meta(source: str, is_sample: bool, count: int) -> None:
    await meta_collection.update_one(
        {"source": source},
        {"$set": {"source": source, "last_updated": datetime.now(timezone.utc),
                   "is_sample": is_sample, "record_count": count}},
        upsert=True,
    )


async def refresh_polymarket() -> None:
    markets, is_sample = await fetch_polymarket_markets()
    await _replace_collection(polymarket_collection, markets)
    await _set_meta("polymarket", is_sample, len(markets))
    logger.info("Refreshed polymarket: %d markets (sample=%s)", len(markets), is_sample)


async def refresh_insiders() -> None:
    filings, is_sample = await fetch_insider_filings()
    await _replace_collection(insiders_collection, filings)
    await _set_meta("insiders", is_sample, len(filings))
    logger.info("Refreshed insiders: %d filings (sample=%s)", len(filings), is_sample)


async def refresh_congress() -> None:
    trades, is_sample = await fetch_congress_trades()
    await _replace_collection(congress_collection, trades)
    await _set_meta("congress", is_sample, len(trades))
    logger.info("Refreshed congress: %d trades (sample=%s)", len(trades), is_sample)


async def refresh_all() -> None:
    for name, fn in (("polymarket", refresh_polymarket), ("insiders", refresh_insiders), ("congress", refresh_congress)):
        try:
            await fn()
        except Exception:
            logger.exception("Refresh failed for source: %s", name)
