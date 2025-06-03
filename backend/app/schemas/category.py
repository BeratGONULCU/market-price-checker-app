from pydantic import BaseModel
from typing import List, Optional
from .base import BaseSchema

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryInDB(CategoryBase, BaseSchema):
    pass

class Category(CategoryInDB):
    id: int
    product_ids: List[int] = []

    class Config:
        from_attributes = True

class CategoryResponse(Category):
    pass 