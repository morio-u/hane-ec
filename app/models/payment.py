from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum


class PaymentStatusEnum(str, Enum):
    unpaid = "unpaid"
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"
    cancelled = "cancelled"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(
        SQLEnum(PaymentStatusEnum), default=PaymentStatusEnum.pending, nullable=False
    )
    transaction_token = Column(String(255), nullable=True)
    paid_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    order = relationship("Order", back_populates="payments")
    user = relationship("User", back_populates="payments")
