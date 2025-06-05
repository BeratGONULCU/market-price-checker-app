from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base import BaseSchema
from .market import Market

class ProductDetailBase(BaseModel):
    product_id: int
    market_id: int
    price: float
    expiration_date: Optional[datetime] = None
    calories: Optional[float] = None

class ProductDetailCreate(ProductDetailBase):
    pass

class ProductDetailUpdate(BaseModel):
    price: Optional[float] = None
    expiration_date: Optional[datetime] = None
    calories: Optional[float] = None

class ProductDetailInDB(ProductDetailBase, BaseSchema):
    pass

class ProductDetail(ProductDetailInDB):
    id: int
    market: Market

    class Config:
        from_attributes = True 