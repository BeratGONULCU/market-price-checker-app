from app.db.session import Base

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.category import Category  # noqa
from app.models.market import Market  # noqa
from app.models.product import Product  # noqa
from app.models.product_detail import ProductDetail  # noqa
from app.models.comment import Comment  # noqa
from app.models.rating import Rating  # noqa
from app.models.price_history import PriceHistory  # noqa
from app.models.price_alert import PriceAlert  # noqa
from app.models.search_history import SearchHistory  # noqa
from app.models.shopping_list_item import ShoppingListItem  # noqa
from app.models.notification import Notification  # noqa
from app.models.user_setting import UserSetting  # noqa
from app.models.favorite import Favorite  # noqa 