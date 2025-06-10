from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class ProductDetail(Base):
    __tablename__ = "product_details"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    market_id = Column(Integer, ForeignKey("markets.id", ondelete="CASCADE"))
    price = Column(Float, nullable=False)
    expiration_date = Column(Date)
    calories = Column(Integer)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="details")
    market = relationship("Market", back_populates="product_details") 