from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from .base import BaseSchema
from .market import Market

class ProductDetailBase(BaseModel):
    product_id: int
    market_id: int
    price: float
    expiration_date: Optional[date] = None
    calories: Optional[int] = None

class ProductDetailCreate(ProductDetailBase):
    pass

class ProductDetailUpdate(ProductDetailBase):
    product_id: Optional[int] = None
    market_id: Optional[int] = None
    price: Optional[float] = None
    expiration_date: Optional[date] = None
    calories: Optional[int] = None

class ProductDetailInDB(ProductDetailBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProductDetail(ProductDetailInDB):
    pass

class ProductDetail(ProductDetailInDB):
    id: int
    market: Market

    class Config:
        from_attributes = True 