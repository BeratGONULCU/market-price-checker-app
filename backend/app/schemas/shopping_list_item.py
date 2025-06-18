from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base import BaseSchema
from .product import Product

class ShoppingListItemBase(BaseModel):
    product_id: int
    quantity: int
    notes: Optional[str] = None

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItemUpdate(ShoppingListItemBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    notes: Optional[str] = None

class ShoppingListItemInDB(ShoppingListItemBase):
    id: int
    shopping_list_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    product: Optional[Product] = None

    class Config:
        from_attributes = True

class ShoppingListItem(ShoppingListItemInDB):
    pass 