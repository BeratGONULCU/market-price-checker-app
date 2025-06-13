from fastapi import APIRouter
from app.api.endpoints import auth, users, products, categories, markets, favorites, shopping_lists

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(markets.router, prefix="/markets", tags=["markets"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
api_router.include_router(shopping_lists.router, prefix="/shopping-lists", tags=["shopping-lists"]) 