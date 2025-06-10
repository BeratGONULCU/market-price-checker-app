from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # İlişkiler
    user = relationship("User", back_populates="favorites")
    product = relationship("Product", back_populates="favorites") 
    market = relationship("Market", back_populates="favorites") 