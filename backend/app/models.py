from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class PolymarketMarket(BaseModel):
    id: str
    question: str
    category: Optional[str] = None
    yes_price: float
    no_price: float
    change_24h: Optional[float] = None
    volume: Optional[float] = None
    liquidity: Optional[float] = None
    end_date: Optional[str] = None
    tickers: list[str] = []
    url: Optional[str] = None
    is_sample: bool = False
    fetched_at: datetime


class InsiderFiling(BaseModel):
    id: str
    ticker: str
    company: str
    insider_name: str
    role: Optional[str] = None
    transaction_type: Literal["buy", "sell"]
    shares: Optional[float] = None
    price_per_share: Optional[float] = None
    value: Optional[float] = None
    filing_date: str
    transaction_date: Optional[str] = None
    source_url: Optional[str] = None
    is_sample: bool = False
    fetched_at: datetime


class CongressTrade(BaseModel):
    id: str
    representative: str
    chamber: Literal["house", "senate"]
    party: Optional[str] = None
    ticker: str
    company: Optional[str] = None
    transaction_type: Literal["buy", "sell", "exchange"]
    amount_range: str
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    transaction_date: str
    disclosure_date: str
    is_sample: bool = False
    fetched_at: datetime


class SourceBreakdown(BaseModel):
    lean: Optional[float] = None
    strength: Optional[float] = None
    count: int = 0


class ConvictionTicker(BaseModel):
    ticker: str
    company: str
    score: float
    direction: Literal["bullish", "bearish", "neutral"]
    high_conviction: bool
    sources_present: list[str]
    congress: SourceBreakdown
    insiders: SourceBreakdown
    polymarket: SourceBreakdown


class ConvictionDetail(ConvictionTicker):
    congress_trades: list[CongressTrade]
    insider_filings: list[InsiderFiling]
    polymarket_markets: list[PolymarketMarket]


class MetaStatus(BaseModel):
    source: str
    last_updated: Optional[datetime] = None
    is_sample: bool
    record_count: int
