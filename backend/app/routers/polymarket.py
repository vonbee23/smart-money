from fastapi import APIRouter, HTTPException

from app.db import polymarket_collection

router = APIRouter(prefix="/api/polymarket", tags=["polymarket"])


@router.get("")
async def list_markets():
    markets = await polymarket_collection.find({}, {"_id": 0}).sort("volume", -1).to_list(length=None)
    return markets


@router.get("/{market_id}")
async def get_market(market_id: str):
    market = await polymarket_collection.find_one({"id": market_id}, {"_id": 0})
    if market is None:
        raise HTTPException(status_code=404, detail="Market not found")
    return market
