from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .base import BaseSchema
from .category import Category

class ProductDetailBase(BaseModel):
    key: str
    value: str
    unit: Optional[str] = None
    product_id: int

class ProductDetailCreate(ProductDetailBase):
    pass

class ProductDetail(ProductDetailBase):
    id: int

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
    prices: List[ProductPrice] = []
    category_ids: List[int] = []
    categories: List[Category] = []

    class Config:
        from_attributes = True 