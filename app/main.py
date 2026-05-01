from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import CompanyFact, NewsItem, Review, Trade
from .schemas import CompanyFactOut, NewsIn, ReviewIn, TradeIn

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Investment Journal API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/company/{ticker}/refresh", response_model=CompanyFactOut)
def refresh_company(ticker: str, db: Session = Depends(get_db)):
    ticker = ticker.upper()
    row = db.query(CompanyFact).filter(CompanyFact.ticker == ticker).first()
    if not row:
        row = CompanyFact(
            ticker=ticker,
            company_name=f"{ticker} Inc.",
            products="Populate from filings/profile ETL",
            consumers="Populate from filings/profile ETL",
            competitors="Populate from filings/profile ETL",
            dependencies="Populate from filings/profile ETL",
            source="on_demand_pipeline",
            source_timestamp=datetime.utcnow(),
            confidence=0.4,
            last_verified_at=datetime.utcnow(),
        )
        db.add(row)
    else:
        row.last_verified_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return row


@app.get("/company/{ticker}/facts", response_model=CompanyFactOut)
def company_facts(ticker: str, db: Session = Depends(get_db)):
    row = db.query(CompanyFact).filter(CompanyFact.ticker == ticker.upper()).first()
    if not row:
        raise HTTPException(status_code=404, detail="Ticker not found. Refresh first.")
    return row


@app.post("/news/ingest")
def ingest_news(payload: NewsIn, db: Session = Depends(get_db)):
    expiry = datetime.utcnow() + timedelta(days=90)
    item = NewsItem(**payload.model_dump(), ticker=payload.ticker.upper(), expires_at=expiry)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id}


@app.get("/news/{ticker}")
def list_news(ticker: str, db: Session = Depends(get_db)):
    rows = (
        db.query(NewsItem)
        .filter(NewsItem.ticker == ticker.upper())
        .order_by(NewsItem.published_at.desc())
        .limit(100)
        .all()
    )
    return rows


@app.post("/news/{item_id}/flag")
def flag_news(item_id: int, db: Session = Depends(get_db)):
    row = db.query(NewsItem).filter(NewsItem.id == item_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="News item not found")
    row.is_flagged = True
    row.expires_at = datetime.utcnow() + timedelta(days=3650)
    db.commit()
    return {"status": "flagged"}


@app.post("/maintenance/news-cleanup")
def cleanup_news(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    old_rows = db.query(NewsItem).filter(NewsItem.expires_at < now, NewsItem.is_flagged.is_(False)).all()
    count = len(old_rows)
    for row in old_rows:
        db.delete(row)
    db.commit()
    return {"deleted": count}


@app.post("/trades")
def create_trade(payload: TradeIn, db: Session = Depends(get_db)):
    trade = Trade(**payload.model_dump(), ticker=payload.ticker.upper())
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return {"id": trade.id}


@app.get("/trades")
def list_trades(db: Session = Depends(get_db)):
    return db.query(Trade).order_by(Trade.created_at.desc()).all()


@app.post("/reviews")
def create_review(payload: ReviewIn, db: Session = Depends(get_db)):
    trade = db.query(Trade).filter(Trade.id == payload.trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    review = Review(**payload.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"id": review.id}
