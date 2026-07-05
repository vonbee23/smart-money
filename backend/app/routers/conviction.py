from fastapi import APIRouter, HTTPException

from app.conviction import build_conviction_board
from app.db import congress_collection, insiders_collection, polymarket_collection

router = APIRouter(prefix="/api/conviction", tags=["conviction"])


async def _load_board() -> list[dict]:
    congress_trades = await congress_collection.find({}, {"_id": 0}).to_list(length=None)
    insider_filings = await insiders_collection.find({}, {"_id": 0}).to_list(length=None)
    polymarket_markets = await polymarket_collection.find({}, {"_id": 0}).to_list(length=None)
    return build_conviction_board(congress_trades, insider_filings, polymarket_markets)


def _public(entry: dict) -> dict:
    return {k: v for k, v in entry.items() if not k.startswith("_")}


@router.get("")
async def list_conviction():
    board = await _load_board()
    return [_public(e) for e in board]


@router.get("/{ticker}")
async def get_conviction_detail(ticker: str):
    board = await _load_board()
    ticker = ticker.upper()
    entry = next((e for e in board if e["ticker"] == ticker), None)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"No data for ticker {ticker}")
    detail = _public(entry)
    detail["congress_trades"] = entry["_congress_trades"]
    detail["insider_filings"] = entry["_insider_filings"]
    detail["polymarket_markets"] = entry["_polymarket_markets"]
    return detail
