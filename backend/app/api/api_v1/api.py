from fastapi import APIRouter
from app.api.endpoints import products, categories, users, auth, favorites

api_router = APIRouter()

# Auth ve Users için trailing slash olmadan
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Diğer endpoint'ler için trailing slash ile
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"]) 