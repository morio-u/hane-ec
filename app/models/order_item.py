from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    sku_id = Column(Integer, ForeignKey("skus.id"), nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    unit_price = Column(DECIMAL(12, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal_amount = Column(DECIMAL(12, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("Order", back_populates="items")
    sku = relationship("SKU", back_populates="order_items")