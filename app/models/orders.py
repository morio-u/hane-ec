from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum

class OrderStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    refunded = "refunded"
    failed = "failed"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True, index=True)
    shipping_last_name = Column(String(50), nullable=False)
    shipping_first_name = Column(String(50), nullable=False)
    shipping_address_line1 = Column(String(100), nullable=False)
    shipping_address_line2 = Column(String(100), nullable=True)
    shipping_city = Column(String(50), nullable=False)
    shipping_state = Column(String(50), nullable=False)
    shipping_zip = Column(String(10), nullable=False)
    shipping_phone_number = Column(String(15), nullable=False)
    total_amount = Column(DECIMAL(12, 2), nullable=False, default=0)
    order_status = Column(SQLEnum(OrderStatusEnum), default=OrderStatusEnum.pending, nullable=False)
    payment_status = Column(SQLEnum(PaymentStatusEnum), default=PaymentStatusEnum.pending, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrederItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")