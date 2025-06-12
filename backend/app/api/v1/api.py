from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, products, markets, shopping_lists, comments

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(markets.router, prefix="/markets", tags=["markets"])
api_router.include_router(shopping_lists.router, prefix="/shopping-lists", tags=["shopping-lists"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"]) 