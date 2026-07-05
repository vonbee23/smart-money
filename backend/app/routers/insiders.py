from fastapi import APIRouter, Query

from app.db import insiders_collection

router = APIRouter(prefix="/api/insiders", tags=["insiders"])


@router.get("")
async def list_insider_filings(buys_only: bool = Query(False)):
    query = {"transaction_type": "buy"} if buys_only else {}
    filings = await insiders_collection.find(query, {"_id": 0}).sort("filing_date", -1).to_list(length=None)
    return filings
