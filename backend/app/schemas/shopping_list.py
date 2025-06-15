from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ShoppingListItemBase(BaseModel):
    product_id: int = Field(..., description="Ürün ID'si")
    quantity: int = Field(1, description="Ürün miktarı")
    notes: Optional[str] = Field(None, description="Ürün için notlar")

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItemUpdate(ShoppingListItemBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = None

class ShoppingListItemInDB(ShoppingListItemBase):
    id: int
    shopping_list_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ShoppingListBase(BaseModel):
    name: str = Field(..., description="Alışveriş listesi adı")

class ShoppingListCreate(ShoppingListBase):
    """
    Yeni alışveriş listesi oluşturmak için kullanılan şema.
    """
    pass

class ShoppingListUpdate(ShoppingListBase):
    name: Optional[str] = None

class ShoppingListInDB(ShoppingListBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    items: List[ShoppingListItemInDB] = []

    class Config:
        from_attributes = True

class ShoppingList(ShoppingListBase):
    id: int
    user_id: int
    items: List[ShoppingListItemInDB]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MarketComparisonItem(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int

class MarketComparisonResponse(BaseModel):
    market_id: int
    market_name: str
    total_price: float
    items: List[MarketComparisonItem]

    class Config:
        orm_mode = True 