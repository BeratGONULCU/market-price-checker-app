from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)  # şuanlık user_id = 1 olarak verilecek ama sonra giriş yapıldığında otomatik olarak alınacak.
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # İlişkiler
    user = relationship("User", back_populates="shopping_lists")
    items = relationship("ShoppingListItem", back_populates="shopping_list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ShoppingList {self.name}>"

class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"

    id = Column(Integer, primary_key=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # İlişkiler
    shopping_list = relationship("ShoppingList", back_populates="items")
    product = relationship("Product", back_populates="shopping_list_items")

    def __repr__(self):
        return f"<ShoppingListItem {self.id}>" 