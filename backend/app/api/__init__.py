from fastapi import APIRouter
from app.api.endpoints import (
    auth,
    categories,
    markets,
    products,
    product_details,
    comments,
    favorites,
    notifications,
    price_alerts,
    price_history,
    ratings,
    search_history,
    shopping_list_items,
    user_settings
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(markets.router, prefix="/markets", tags=["markets"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(product_details.router, prefix="/product-details", tags=["product-details"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(price_alerts.router, prefix="/price-alerts", tags=["price-alerts"])
api_router.include_router(price_history.router, prefix="/price-history", tags=["price-history"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
api_router.include_router(search_history.router, prefix="/search-history", tags=["search-history"])
api_router.include_router(shopping_list_items.router, prefix="/shopping-list-items", tags=["shopping-list-items"])
api_router.include_router(user_settings.router, prefix="/user-settings", tags=["user-settings"]) 