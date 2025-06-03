from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.market import Market
from app.schemas.market import Market as MarketSchema, MarketCreate, MarketUpdate

router = APIRouter()

@router.post("/", response_model=MarketSchema)
def create_market(market: MarketCreate, db: Session = Depends(get_db)):
    db_market = Market(**market.dict())
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

@router.get("/", response_model=List[MarketSchema])
def read_markets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    markets = db.query(Market).offset(skip).limit(limit).all()
    return markets

@router.get("/{market_id}", response_model=MarketSchema)
def read_market(market_id: int, db: Session = Depends(get_db)):
    db_market = db.query(Market).filter(Market.id == market_id).first()
    if db_market is None:
        raise HTTPException(status_code=404, detail="Market not found")
    return db_market

@router.put("/{market_id}", response_model=MarketSchema)
def update_market(market_id: int, market: MarketUpdate, db: Session = Depends(get_db)):
    db_market = db.query(Market).filter(Market.id == market_id).first()
    if db_market is None:
        raise HTTPException(status_code=404, detail="Market not found")
    
    for key, value in market.dict(exclude_unset=True).items():
        setattr(db_market, key, value)
    
    db.commit()
    db.refresh(db_market)
    return db_market

@router.delete("/{market_id}", response_model=MarketSchema)
def delete_market(market_id: int, db: Session = Depends(get_db)):
    db_market = db.query(Market).filter(Market.id == market_id).first()
    if db_market is None:
        raise HTTPException(status_code=404, detail="Market not found")
    
    db.delete(db_market)
    db.commit()
    return db_market 