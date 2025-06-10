from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class PriceAlert(Base):
    __tablename__ = "price_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    target_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_checked = Column(DateTime)
    notified = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="price_alerts")
    product = relationship("Product", back_populates="price_alerts") 