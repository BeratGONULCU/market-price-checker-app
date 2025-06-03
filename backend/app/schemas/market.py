from pydantic import BaseModel
from typing import Optional
from .base import BaseSchema

class MarketBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    open_hours: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class MarketCreate(MarketBase):
    pass

class MarketUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    open_hours: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class MarketInDB(MarketBase, BaseSchema):
    pass

class Market(MarketInDB):
    pass 