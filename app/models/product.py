from sqlalchemy import Column, Integer, String, Text, Enum, DECIMAL, TIMESTAMP, CHAR, SmallInteger, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum


class PurchaseTypeEnum(Enum):
    consignment = 0
    purchase = 1
    in_house = 2
    other = 3

class ProductStatusEnum(Enum):
    draft = "draft"
    active = "active"
    inactive = "inactive"
    discontinued = "discontinued"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    internal_part_number = Column(CHAR(13), unique=True, nullable=False)
    manufacturer_part_number = Column(String(50), nullable=True)
    subcategory_id = Column(SmallInteger, ForeignKey("subcategories.id"), nullable=False)
    brand_id = Column(SmallInteger, ForeignKey("brands.id"), nullable=False)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=True)
    shipping_rule_id = Column(Integer, ForeignKey("shipping_rules.id"), nullable=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    purchase_type = Column(Enum(PurchaseTypeEnum), nullable=False)
    price_excluding_tax = Column(DECIMAL(12, 2), nullable=True)
    cost_price = Column(DECIMAL(12, 2), nullable=True)
    status = Column(Enum(ProductStatusEnum), default=ProductStatusEnum.inactive, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)