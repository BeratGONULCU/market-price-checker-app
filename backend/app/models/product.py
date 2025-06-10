from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Many-to-many relationship table for products and categories
product_category = Table(
    'product_category',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    brand = Column(String(100))
    image_url = Column(String(255))
    barcode = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    categories = relationship("Category", secondary=product_category, back_populates="products")
    details = relationship("ProductDetail", back_populates="product", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="product", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="product", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    price_alerts = relationship("PriceAlert", back_populates="product", cascade="all, delete-orphan")
    search_history = relationship("SearchHistory", back_populates="product", cascade="all, delete-orphan")
    shopping_list_items = relationship("ShoppingListItem", back_populates="product", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="product", cascade="all, delete-orphan")

    # Diğer ilişkiler ve alanlar burada kalabilir 