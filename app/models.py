from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class CompanyFact(Base):
    __tablename__ = "company_facts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255))
    sector: Mapped[str] = mapped_column(String(128), default="Unknown")
    industry: Mapped[str] = mapped_column(String(128), default="Unknown")
    products: Mapped[str] = mapped_column(Text, default="")
    consumers: Mapped[str] = mapped_column(Text, default="")
    competitors: Mapped[str] = mapped_column(Text, default="")
    dependencies: Mapped[str] = mapped_column(Text, default="")
    source: Mapped[str] = mapped_column(String(255), default="manual_pipeline")
    source_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    last_verified_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NewsItem(Base):
    __tablename__ = "news_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(16), index=True)
    published_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    source_name: Mapped[str] = mapped_column(String(128))
    source_type: Mapped[str] = mapped_column(String(64), default="media_article")
    headline: Mapped[str] = mapped_column(String(512))
    summary: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(String(1024))
    tags: Mapped[str] = mapped_column(String(255), default="")
    sentiment: Mapped[str] = mapped_column(String(32), default="neutral")
    is_flagged: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(16), index=True)
    strategy: Mapped[str] = mapped_column(String(128))
    direction: Mapped[str] = mapped_column(String(16))
    thesis: Mapped[str] = mapped_column(Text)
    risk_plan: Mapped[str] = mapped_column(Text)
    invalidation: Mapped[str] = mapped_column(Text)
    entry_trigger: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trade_id: Mapped[int] = mapped_column(Integer, index=True)
    outcome: Mapped[str] = mapped_column(String(64))
    lessons: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
