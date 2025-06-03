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
    pass

class MarketBase(BaseModel):
    name: str
    address: str
    phone: str
    open_hours: str
    latitude: float
    longitude: float

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

class ProductDetailBase(BaseModel):
    price: float
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
    product_id: int

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
    product_id: int
    market_id: int

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
    
    class Config:
        from_attributes = True

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class Comment(CommentBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Favorite(FavoriteBase):
    id: int
    user_id: int
    product_id: int
    
    class Config:
        from_attributes = True

class Market(MarketBase):
    id: int
    
    class Config:
        from_attributes = True

class Notification(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PriceAlert(PriceAlertBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    last_checked: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PriceHistory(PriceHistoryBase):
    id: int
    product_id: int
    market_id: int
    recorded_at: datetime
    
    class Config:
        from_attributes = True

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True

class ProductDetail(ProductDetailBase):
    id: int
    product_id: int
    market_id: int
    recorded_at: datetime
    last_updated: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Rating(RatingBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SearchHistory(SearchHistoryBase):
    id: int
    user_id: int
    searched_at: datetime
    
    class Config:
        from_attributes = True

class ShoppingListItem(ShoppingListItemBase):
    id: int
    user_id: int
    product_id: int
    
    class Config:
        from_attributes = True

class UserSetting(UserSettingBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True 