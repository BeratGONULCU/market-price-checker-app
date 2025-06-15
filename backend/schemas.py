from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    barcode: Optional[str] = None
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ShoppingListItemBase(BaseModel):
    product_id: int
    quantity: int
    notes: Optional[str] = None

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItem(ShoppingListItemBase):
    id: int
    shopping_list_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    product: Product

    class Config:
        from_attributes = True

class ShoppingListBase(BaseModel):
    name: str

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingList(ShoppingListBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[ShoppingListItem] = []

    class Config:
        from_attributes = True 