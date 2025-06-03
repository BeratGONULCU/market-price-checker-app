from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from . import models, schemas
from .core.security import get_password_hash

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Category CRUD
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(
        name=category.name,
        description=category.description,
        parent_id=category.parent_id if category.parent_id else None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = get_category(db, category_id=category_id)
    if db_category:
        update_data = category.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id=category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# Comment CRUD
def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()

def get_product_comments(db: Session, product_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).filter(models.Comment.product_id == product_id).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(**comment.dict(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Favorite CRUD
def get_favorite(db: Session, favorite_id: int):
    return db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()

def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).offset(skip).limit(limit).all()

def create_favorite(db: Session, favorite: schemas.FavoriteCreate, user_id: int):
    db_favorite = models.Favorite(**favorite.dict(), user_id=user_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def delete_favorite(db: Session, favorite_id: int, user_id: int):
    db_favorite = db.query(models.Favorite).filter(
        models.Favorite.id == favorite_id,
        models.Favorite.user_id == user_id
    ).first()
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
    return db_favorite

# Market CRUD
def get_market(db: Session, market_id: int):
    return db.query(models.Market).filter(models.Market.id == market_id).first()

def get_markets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Market).offset(skip).limit(limit).all()

def create_market(db: Session, market: schemas.MarketCreate):
    db_market = models.Market(**market.dict())
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

# Notification CRUD
def get_notification(db: Session, notification_id: int):
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()

def get_user_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).offset(skip).limit(limit).all()

def create_notification(db: Session, notification: schemas.NotificationCreate, user_id: int):
    db_notification = models.Notification(**notification.dict(), user_id=user_id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def mark_notification_as_read(db: Session, notification_id: int, user_id: int):
    db_notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == user_id
    ).first()
    if db_notification:
        db_notification.is_read = True
        db_notification.read_at = datetime.now()
        db.commit()
        db.refresh(db_notification)
    return db_notification

# PriceAlert CRUD
def get_price_alert(db: Session, alert_id: int):
    return db.query(models.PriceAlert).filter(models.PriceAlert.id == alert_id).first()

def get_user_price_alerts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.PriceAlert).filter(models.PriceAlert.user_id == user_id).offset(skip).limit(limit).all()

def create_price_alert(db: Session, alert: schemas.PriceAlertCreate, user_id: int):
    db_alert = models.PriceAlert(**alert.dict(), user_id=user_id)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def update_price_alert(db: Session, alert_id: int, alert: schemas.PriceAlert, user_id: int):
    db_alert = db.query(models.PriceAlert).filter(
        models.PriceAlert.id == alert_id,
        models.PriceAlert.user_id == user_id
    ).first()
    if db_alert:
        for key, value in alert.dict().items():
            setattr(db_alert, key, value)
        db.commit()
        db.refresh(db_alert)
    return db_alert

# PriceHistory CRUD
def get_price_history(db: Session, history_id: int):
    return db.query(models.PriceHistory).filter(models.PriceHistory.id == history_id).first()

def get_product_price_history(db: Session, product_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.PriceHistory).filter(
        models.PriceHistory.product_id == product_id
    ).order_by(desc(models.PriceHistory.recorded_at)).offset(skip).limit(limit).all()

def create_price_history(db: Session, history: schemas.PriceHistoryCreate):
    db_history = models.PriceHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict(exclude={'category_ids'}))
    if product.category_ids:
        categories = db.query(models.Category).filter(models.Category.id.in_(product.category_ids)).all()
        db_product.categories = categories
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# ProductDetail CRUD
def get_product_detail(db: Session, detail_id: int):
    return db.query(models.ProductDetail).filter(models.ProductDetail.id == detail_id).first()

def get_product_details(db: Session, product_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ProductDetail).filter(
        models.ProductDetail.product_id == product_id
    ).offset(skip).limit(limit).all()

def create_product_detail(db: Session, detail: schemas.ProductDetailCreate):
    db_detail = models.ProductDetail(**detail.dict())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

# Rating CRUD
def get_rating(db: Session, rating_id: int):
    return db.query(models.Rating).filter(models.Rating.id == rating_id).first()

def get_product_ratings(db: Session, product_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Rating).filter(models.Rating.product_id == product_id).offset(skip).limit(limit).all()

def create_rating(db: Session, rating: schemas.RatingCreate, user_id: int):
    db_rating = models.Rating(**rating.dict(), user_id=user_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

# SearchHistory CRUD
def get_search_history(db: Session, history_id: int):
    return db.query(models.SearchHistory).filter(models.SearchHistory.id == history_id).first()

def get_user_search_history(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.SearchHistory).filter(
        models.SearchHistory.user_id == user_id
    ).order_by(desc(models.SearchHistory.searched_at)).offset(skip).limit(limit).all()

def create_search_history(db: Session, history: schemas.SearchHistoryCreate, user_id: int):
    db_history = models.SearchHistory(**history.dict(), user_id=user_id)
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

# ShoppingListItem CRUD
def get_shopping_list_item(db: Session, item_id: int):
    return db.query(models.ShoppingListItem).filter(models.ShoppingListItem.id == item_id).first()

def get_user_shopping_list(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ShoppingListItem).filter(
        models.ShoppingListItem.user_id == user_id
    ).offset(skip).limit(limit).all()

def create_shopping_list_item(db: Session, item: schemas.ShoppingListItemCreate, user_id: int):
    db_item = models.ShoppingListItem(**item.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_shopping_list_item(db: Session, item_id: int, item: schemas.ShoppingListItem, user_id: int):
    db_item = db.query(models.ShoppingListItem).filter(
        models.ShoppingListItem.id == item_id,
        models.ShoppingListItem.user_id == user_id
    ).first()
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

# UserSetting CRUD
def get_user_setting(db: Session, setting_id: int):
    return db.query(models.UserSetting).filter(models.UserSetting.id == setting_id).first()

def get_user_settings(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.UserSetting).filter(
        models.UserSetting.user_id == user_id
    ).offset(skip).limit(limit).all()

def create_user_setting(db: Session, setting: schemas.UserSettingCreate, user_id: int):
    db_setting = models.UserSetting(**setting.dict(), user_id=user_id)
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

def update_user_setting(db: Session, setting_id: int, setting: schemas.UserSetting, user_id: int):
    db_setting = db.query(models.UserSetting).filter(
        models.UserSetting.id == setting_id,
        models.UserSetting.user_id == user_id
    ).first()
    if db_setting:
        for key, value in setting.dict().items():
            setattr(db_setting, key, value)
        db.commit()
        db.refresh(db_setting)
    return db_setting 