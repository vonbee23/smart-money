from fastapi import APIRouter

from app.cache import refresh_all
from app.db import meta_collection

router = APIRouter(prefix="/api", tags=["meta"])


@router.get("/meta")
async def get_meta():
    return await meta_collection.find({}, {"_id": 0}).to_list(length=None)


@router.post("/refresh")
async def trigger_refresh():
    await refresh_all()
    return await meta_collection.find({}, {"_id": 0}).to_list(length=None)
