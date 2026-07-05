import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.cache import refresh_all
from app.config import settings
from app.routers import congress, conviction, insiders, meta, polymarket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await refresh_all()
    scheduler.add_job(refresh_all, "interval", minutes=settings.refresh_interval_minutes,
                       id="refresh_all", replace_existing=True)
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(title="Smart Money API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conviction.router)
app.include_router(polymarket.router)
app.include_router(insiders.router)
app.include_router(congress.router)
app.include_router(meta.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
