from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db_name]

polymarket_collection = db["polymarket_markets"]
insiders_collection = db["insider_filings"]
congress_collection = db["congress_trades"]
meta_collection = db["meta"]
