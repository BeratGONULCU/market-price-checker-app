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
    
    # Create tables in the correct order
    # First create tables without foreign keys
    User.__table__.create(engine)
    Category.__table__.create(engine)
    Market.__table__.create(engine)
    
    # Then create tables with foreign keys
    Product.__table__.create(engine)
    ProductDetail.__table__.create(engine)
    Comment.__table__.create(engine)
    Favorite.__table__.create(engine)
    Notification.__table__.create(engine)
    PriceAlert.__table__.create(engine)
    PriceHistory.__table__.create(engine)
    Rating.__table__.create(engine)
    SearchHistory.__table__.create(engine)
    ShoppingListItem.__table__.create(engine)
    UserSetting.__table__.create(engine) 