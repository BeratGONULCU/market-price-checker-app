from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
from app.models.category import product_categories
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    brand = Column(String(100))
    image_url = Column(String(255))
    barcode = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    categories = relationship("Category", secondary=product_categories, back_populates="products")
    details = relationship("ProductDetail", back_populates="product")
    comments = relationship("Comment", back_populates="product")
    favorites = relationship("Favorite", back_populates="product")
    price_history = relationship("PriceHistory", back_populates="product")
    ratings = relationship("Rating", back_populates="product")
    shopping_list_items = relationship("ShoppingListItem", back_populates="product")
    price_alerts = relationship("PriceAlert", back_populates="product")

    # Diğer ilişkiler ve alanlar burada kalabilir 