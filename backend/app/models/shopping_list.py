from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    user = relationship("User", back_populates="shopping_lists")
    items = relationship("ShoppingListItem", back_populates="shopping_list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ShoppingList {self.id}>"

class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"

    id = Column(Integer, primary_key=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    shopping_list = relationship("ShoppingList", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<ShoppingListItem {self.id}>" 