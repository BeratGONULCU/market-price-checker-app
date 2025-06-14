from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.market import Market
from app.schemas.market import MarketCreate, MarketUpdate

def get_market(db: Session, market_id: int) -> Optional[Market]:
    """Get a market by ID."""
    return db.query(Market).filter(Market.id == market_id).first()

def get_markets(db: Session, skip: int = 0, limit: int = 100) -> List[Market]:
    """Get all markets with pagination."""
    return db.query(Market).offset(skip).limit(limit).all()

def create_market(db: Session, market: MarketCreate) -> Market:
    """Create a new market."""
    db_market = Market(**market.dict())
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

def update_market(db: Session, market_id: int, market: MarketUpdate) -> Optional[Market]:
    """Update a market."""
    db_market = get_market(db, market_id)
    if db_market:
        for key, value in market.dict(exclude_unset=True).items():
            setattr(db_market, key, value)
        db.commit()
        db.refresh(db_market)
    return db_market

def delete_market(db: Session, market_id: int) -> bool:
    """Delete a market."""
    db_market = get_market(db, market_id)
    if db_market:
        db.delete(db_market)
        db.commit()
        return True
    return False 