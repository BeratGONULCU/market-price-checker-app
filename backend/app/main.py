from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.api import api_router
from app.api.auth import router as auth_router
from app.core.config import settings
from app import crud, models
from app.schemas import (
    User, UserCreate, Category, CategoryCreate, Comment, CommentCreate,
    Favorite, FavoriteCreate, Market, MarketCreate, Notification, NotificationCreate,
    PriceAlert, PriceAlertBase, PriceAlertCreate, PriceHistory, PriceHistoryCreate,
    Product, ProductCreate, ProductDetail, ProductDetailCreate, Rating, RatingCreate,
    SearchHistory, SearchHistoryCreate, ShoppingListItem, ShoppingListItemBase,
    ShoppingListItemCreate, UserSetting, UserSettingBase, UserSettingCreate
)
from app.database import SessionLocal, engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_router, prefix=settings.API_V1_STR)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User endpoints
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Category endpoints
@app.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Comment endpoints
@app.post("/comments/", response_model=Comment)
def create_comment(comment: CommentCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, user_id=user_id)

@app.get("/comments/", response_model=List[Comment])
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, skip=skip, limit=limit)
    return comments

@app.get("/products/{product_id}/comments/", response_model=List[Comment])
def read_product_comments(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_product_comments(db, product_id=product_id, skip=skip, limit=limit)
    return comments

# Favorite endpoints
@app.post("/favorites/", response_model=Favorite)
def create_favorite(favorite: FavoriteCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_favorite(db=db, favorite=favorite, user_id=user_id)

@app.get("/users/{user_id}/favorites/", response_model=List[Favorite])
def read_user_favorites(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    favorites = crud.get_user_favorites(db, user_id=user_id, skip=skip, limit=limit)
    return favorites

@app.delete("/favorites/{favorite_id}")
def delete_favorite(favorite_id: int, user_id: int, db: Session = Depends(get_db)):
    favorite = crud.delete_favorite(db=db, favorite_id=favorite_id, user_id=user_id)
    if favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Favorite deleted successfully"}

# Market endpoints
@app.post("/markets/", response_model=Market)
def create_market(market: MarketCreate, db: Session = Depends(get_db)):
    return crud.create_market(db=db, market=market)

@app.get("/markets/", response_model=List[Market])
def read_markets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    markets = crud.get_markets(db, skip=skip, limit=limit)
    return markets

@app.get("/markets/{market_id}", response_model=Market)
def read_market(market_id: int, db: Session = Depends(get_db)):
    db_market = crud.get_market(db, market_id=market_id)
    if db_market is None:
        raise HTTPException(status_code=404, detail="Market not found")
    return db_market

# Notification endpoints
@app.post("/notifications/", response_model=Notification)
def create_notification(notification: NotificationCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_notification(db=db, notification=notification, user_id=user_id)

@app.get("/users/{user_id}/notifications/", response_model=List[Notification])
def read_user_notifications(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notifications = crud.get_user_notifications(db, user_id=user_id, skip=skip, limit=limit)
    return notifications

@app.put("/notifications/{notification_id}/read")
def mark_notification_as_read(notification_id: int, user_id: int, db: Session = Depends(get_db)):
    notification = crud.mark_notification_as_read(db=db, notification_id=notification_id, user_id=user_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}

# PriceAlert endpoints
@app.post("/price-alerts/", response_model=PriceAlert)
def create_price_alert(alert: PriceAlertCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_price_alert(db=db, alert=alert, user_id=user_id)

@app.get("/users/{user_id}/price-alerts/", response_model=List[PriceAlert])
def read_user_price_alerts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = crud.get_user_price_alerts(db, user_id=user_id, skip=skip, limit=limit)
    return alerts

@app.put("/price-alerts/{alert_id}")
def update_price_alert(alert_id: int, alert: PriceAlertBase, user_id: int, db: Session = Depends(get_db)):
    db_alert = crud.update_price_alert(db=db, alert_id=alert_id, alert=alert, user_id=user_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Price alert not found")
    return {"message": "Price alert updated successfully"}

# PriceHistory endpoints
@app.post("/price-history/", response_model=PriceHistory)
def create_price_history(history: PriceHistoryCreate, db: Session = Depends(get_db)):
    return crud.create_price_history(db=db, history=history)

@app.get("/products/{product_id}/price-history/", response_model=List[PriceHistory])
def read_product_price_history(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    history = crud.get_product_price_history(db, product_id=product_id, skip=skip, limit=limit)
    return history

# Product endpoints
@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# ProductDetail endpoints
@app.post("/product-details/", response_model=ProductDetail)
def create_product_detail(detail: ProductDetailCreate, db: Session = Depends(get_db)):
    return crud.create_product_detail(db=db, detail=detail)

@app.get("/products/{product_id}/details/", response_model=List[ProductDetail])
def read_product_details(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    details = crud.get_product_details(db, product_id=product_id, skip=skip, limit=limit)
    return details

# Rating endpoints
@app.post("/ratings/", response_model=Rating)
def create_rating(rating: RatingCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_rating(db=db, rating=rating, user_id=user_id)

@app.get("/products/{product_id}/ratings/", response_model=List[Rating])
def read_product_ratings(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ratings = crud.get_product_ratings(db, product_id=product_id, skip=skip, limit=limit)
    return ratings

# SearchHistory endpoints
@app.post("/search-history/", response_model=SearchHistory)
def create_search_history(history: SearchHistoryCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_search_history(db=db, history=history, user_id=user_id)

@app.get("/users/{user_id}/search-history/", response_model=List[SearchHistory])
def read_user_search_history(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    history = crud.get_user_search_history(db, user_id=user_id, skip=skip, limit=limit)
    return history

# ShoppingListItem endpoints
@app.post("/shopping-list/", response_model=ShoppingListItem)
def create_shopping_list_item(item: ShoppingListItemCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_shopping_list_item(db=db, item=item, user_id=user_id)

@app.get("/users/{user_id}/shopping-list/", response_model=List[ShoppingListItem])
def read_user_shopping_list(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_user_shopping_list(db, user_id=user_id, skip=skip, limit=limit)
    return items

@app.put("/shopping-list/{item_id}")
def update_shopping_list_item(item_id: int, item: ShoppingListItemBase, user_id: int, db: Session = Depends(get_db)):
    db_item = crud.update_shopping_list_item(db=db, item_id=item_id, item=item, user_id=user_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shopping list item not found")
    return {"message": "Shopping list item updated successfully"}

# UserSetting endpoints
@app.post("/user-settings/", response_model=UserSetting)
def create_user_setting(setting: UserSettingCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_user_setting(db=db, setting=setting, user_id=user_id)

@app.get("/users/{user_id}/settings/", response_model=List[UserSetting])
def read_user_settings(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    settings = crud.get_user_settings(db, user_id=user_id, skip=skip, limit=limit)
    return settings

@app.put("/user-settings/{setting_id}")
def update_user_setting(setting_id: int, setting: UserSettingBase, user_id: int, db: Session = Depends(get_db)):
    db_setting = crud.update_user_setting(db=db, setting_id=setting_id, setting=setting, user_id=user_id)
    if db_setting is None:
        raise HTTPException(status_code=404, detail="User setting not found")
    return {"message": "User setting updated successfully"}

@app.get("/")
def root():
    return {"message": "Welcome to Market Price Comparison API"}
