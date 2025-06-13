from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .base import BaseSchema
from .category import Category
from .product_detail import ProductDetail
from .market import Market

class ProductDetailBase(BaseModel):
    product_id: int
    market_id: int
    price: float
    expiration_date: Optional[datetime] = None
    calories: Optional[float] = None

class ProductDetailCreate(ProductDetailBase):
    pass

class ProductDetail(ProductDetailBase):
    id: int
    market: Optional[Market] = None

    class Config:
        from_attributes = True

class ProductPriceBase(BaseModel):
    price: float
    market_id: int
    product_id: int

class ProductPriceCreate(ProductPriceBase):
    pass

class ProductPrice(ProductPriceBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    barcode: Optional[str] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    category_ids: Optional[List[int]] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    barcode: Optional[str] = None
    category_ids: Optional[List[int]] = None

class ProductInDB(ProductBase, BaseSchema):
    pass

class Product(ProductInDB):
    id: int
    details: List[ProductDetail] = []
    category_ids: List[int] = []
    categories: List[Category] = []

    class Config:
        from_attributes = True 