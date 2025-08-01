from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CommentBase(BaseModel):
    content: str

class FavoriteBase(BaseModel):
    user_id: int
    product_id: int
    market_id: int

class MarketBase(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    image_url: Optional[str] = None

class NotificationBase(BaseModel):
    title: str
    message: str
    type: str

class PriceAlertBase(BaseModel):
    target_price: float
    is_active: bool = True
    notified: bool = False

class PriceHistoryBase(BaseModel):
    price: float

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    barcode: Optional[str] = None
    image_url: Optional[str] = None
    category_id: int

class ProductDetailBase(BaseModel):
    product_id: int
    market_id: int
    price: float
    url: Optional[str] = None
    expiration_date: Optional[datetime] = None
    calories: Optional[float] = None

class RatingBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class SearchHistoryBase(BaseModel):
    keyword: str

class ShoppingListItemBase(BaseModel):
    is_checked: bool = False

class UserSettingBase(BaseModel):
    setting_key: str
    value: str

# Create schemas
class UserCreate(UserBase):
    password: str

class CategoryCreate(CategoryBase):
    pass

class CommentCreate(CommentBase):
    product_id: int

class FavoriteCreate(FavoriteBase):
    pass

class MarketCreate(MarketBase):
    pass

class NotificationCreate(NotificationBase):
    pass

class PriceAlertCreate(PriceAlertBase):
    product_id: int

class PriceHistoryCreate(PriceHistoryBase):
    product_id: int
    market_id: int

class ProductCreate(ProductBase):
    category_ids: Optional[List[int]] = None

class ProductDetailCreate(ProductDetailBase):
    pass

class RatingCreate(RatingBase):
    product_id: int

class SearchHistoryCreate(SearchHistoryBase):
    pass

class ShoppingListItemCreate(ShoppingListItemBase):
    product_id: int

class UserSettingCreate(UserSettingBase):
    pass

# Response schemas
class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True

class Category(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True

class Comment(CommentBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class Favorite(FavoriteBase):
    id: int
    
    class Config:
        orm_mode = True

class Market(MarketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Notification(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class PriceAlert(PriceAlertBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    last_checked: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class PriceHistory(PriceHistoryBase):
    id: int
    product_id: int
    market_id: int
    recorded_at: datetime
    
    class Config:
        orm_mode = True

class Product(ProductBase):
    id: int
    details: List[ProductDetail]
    category: Category
    
    class Config:
        orm_mode = True

class ProductDetail(ProductDetailBase):
    id: int
    market: Market
    recorded_at: datetime
    last_updated: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class Rating(RatingBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class SearchHistory(SearchHistoryBase):
    id: int
    user_id: int
    searched_at: datetime
    
    class Config:
        orm_mode = True

class ShoppingListItem(ShoppingListItemBase):
    id: int
    user_id: int
    product_id: int
    
    class Config:
        orm_mode = True

class UserSetting(UserSettingBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 