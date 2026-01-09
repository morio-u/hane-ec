from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    TIMESTAMP,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from enum import Enum


class OrderStatusEnum(str, Enum):
    created = "created"
    confirmed = "confirmed"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    returned = "returned"


class PaymentStatusEnum(str, Enum):
    unpaid = "unpaid"
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"
    cancelled = "cancelled"


class ShippingStatusEnum(str, Enum):
    not_required = "not_required"
    unshipped = "unshipped"
    preparing = "preparing"
    shipped = "shipped"
    delivered = "delivered"
    returned = "returned"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    shipping_last_name = Column(String(50), nullable=False)
    shipping_first_name = Column(String(50), nullable=False)
    shipping_address_line1 = Column(String(100), nullable=False)
    shipping_address_line2 = Column(String(100), nullable=True)
    shipping_city = Column(String(50), nullable=False)
    shipping_state = Column(String(50), nullable=False)
    shipping_zip = Column(String(10), nullable=False)
    shipping_phone_number = Column(String(15), nullable=False)
    subtotal_amount = Column(DECIMAL(12, 2), nullable=False, default=0)
    tax_amount = Column(DECIMAL(12, 2), nullable=False, default=0)
    shipping_fee = Column(DECIMAL(12, 2), nullable=False, default=0)
    payment_processing_fee = Column(DECIMAL(12, 2), nullable=False, default=0)
    total_amount = Column(DECIMAL(12, 2), nullable=False, default=0)
    shipping_method = Column(String(50), nullable=False)
    order_status = Column(
        SQLEnum(OrderStatusEnum), default=OrderStatusEnum.created, nullable=False
    )
    shipping_status = Column(
        SQLEnum(ShippingStatusEnum),
        default=ShippingStatusEnum.unshipped,
        nullable=False,
    )
    payment_status = Column(
        SQLEnum(PaymentStatusEnum), default=PaymentStatusEnum.pending, nullable=False
    )
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", back_populates="orders")
    order_items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    payments = relationship(
        "Payment", back_populates="order", cascade="all, delete-orphan"
    )
