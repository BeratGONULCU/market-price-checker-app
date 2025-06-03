from app.db.session import Base

# Import all models here for Alembic
# This is needed for Alembic to detect all models
# Do not remove this import
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.market import Market
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