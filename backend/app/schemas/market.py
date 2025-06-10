from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MarketBase(BaseModel):
    name: str
    website: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    open_hours: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class MarketCreate(MarketBase):
    pass

class MarketUpdate(MarketBase):
    pass

class Market(MarketBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 