from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine
from app.models import Base

# Import all models to ensure they are registered with Base
from app.models.user import User
from app.models.category import Category
from app.models.market import Market
from app.models.product import Product
from app.models.product_detail import ProductDetail
from app.models.comment import Comment
from app.models.favorite import Favorite
from app.models.notification import Notification
from app.models.price_alert import PriceAlert
from app.models.price_history import PriceHistory
from app.models.rating import Rating
from app.models.search_history import SearchHistory
from app.models.shopping_list import ShoppingList
from app.models.shopping_list_item import ShoppingListItem
from app.models.user_setting import UserSetting

def init_db():
    # Drop all tables first to ensure clean state
    with engine.connect() as conn:
        # Disable foreign key constraints temporarily
        conn.execute(text("SET session_replication_role = 'replica';"))
        
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        
        # Re-enable foreign key constraints
        conn.execute(text("SET session_replication_role = 'origin';"))
        conn.commit()
    
    # Create all tables
    Base.metadata.create_all(bind=engine) 