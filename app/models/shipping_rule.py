from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, DECIMAL
from sqlalchemy.sql import func
from app.database import Base


class ShippingRule(Base):
    __tablename__ = "shipping_rules"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
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