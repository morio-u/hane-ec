from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class ShippingRule(Base):
    __tablename__ = "shipping_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    min_weight = Column(DECIMAL(10, 2))
    max_weight = Column(DECIMAL(10, 2))
    min_size = Column(DECIMAL(10, 2))
    max_size = Column(DECIMAL(10, 2))
    fee = Column(DECIMAL(10, 2), nullable=False)
    area = Column(String(50), default="mainland")
    carrier = Column(String(50))
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="shipping_rule")
