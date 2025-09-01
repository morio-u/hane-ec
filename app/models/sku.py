from sqlalchemy import Column, Integer, Enum, DECIMAL, TIMESTAMP, CHAR, SmallInteger, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum


class SkuStatusEnum(Enum):
    active = "active"
    out_of_stock = "out_of_stock"
    inactive = "inactive"
    discontinued = "discontinued"

class Sku(Base):
    __tablename__ = "skus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    internal_part_number_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    upc = Column(CHAR(12), unique=True, nullable=False)
    color_id = Column(SmallInteger, ForeignKey("colors.id"), nullable=True)
    size_id = Column(SmallInteger, ForeignKey("sizes.id"), nullable=True)
    stock_quantity = Column(SmallInteger, nullable=False)
    special_price = Column(DECIMAL(12, 2), nullable=True)
    status = Column(Enum(SkuStatusEnum), default=SkuStatusEnum.inactive, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)