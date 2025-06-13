from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseSchema

class MarketBase(BaseModel):
    name: str
    website: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    open_hours: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None

class MarketCreate(MarketBase):
    pass

class MarketUpdate(MarketBase):
    pass

class MarketInDB(MarketBase, BaseSchema):
    pass

class Market(MarketInDB):
    id: int

    class Config:
        from_attributes = True 