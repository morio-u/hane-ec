from sqlalchemy import Column, Integer, Enum as SQLEnum, DECIMAL, TIMESTAMP, String, SmallInteger, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum


class SkuStatusEnum(str, Enum):
    active = "active"
    out_of_stock = "out_of_stock"
    inactive = "inactive"
    discontinued = "discontinued"

class Sku(Base):
    __tablename__ = "skus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    barcode = Column(String(13), unique=True, nullable=False)
    color_id = Column(SmallInteger, ForeignKey("colors.id"), nullable=True, index=True)
    size_id = Column(SmallInteger, ForeignKey("sizes.id"), nullable=True, index=True)
    stock_quantity = Column(Integer, nullable=False)
    special_price = Column(DECIMAL(12, 2), nullable=True)
    status = Column(SQLEnum(SkuStatusEnum), default=SkuStatusEnum.inactive, nullable=False, index=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    product = relationship("Product", back_populates="skus")
    color = relationship("Color", back_populates="skus")
    size = relationship("Size", back_populates="skus")
    order_items = relationship("OrderItem", back_populates="sku")