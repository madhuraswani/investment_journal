from datetime import datetime

from pydantic import BaseModel


class CompanyFactOut(BaseModel):
    ticker: str
    company_name: str
    sector: str
    industry: str
    products: str
    consumers: str
    competitors: str
    dependencies: str
    source: str
    confidence: float

    class Config:
        from_attributes = True


class NewsIn(BaseModel):
    ticker: str
    published_at: datetime
    source_name: str
    source_type: str = "media_article"
    headline: str
    summary: str = ""
    url: str
    tags: str = ""
    sentiment: str = "neutral"


class TradeIn(BaseModel):
    ticker: str
    strategy: str
    direction: str
    thesis: str
    risk_plan: str
    invalidation: str
    entry_trigger: str


class ReviewIn(BaseModel):
    trade_id: int
    outcome: str
    lessons: str
