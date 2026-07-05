from fastapi import APIRouter

from app.db import congress_collection

router = APIRouter(prefix="/api/congress", tags=["congress"])


@router.get("")
async def list_congress_trades():
    trades = await congress_collection.find({}, {"_id": 0}).sort("disclosure_date", -1).to_list(length=None)
    return trades
