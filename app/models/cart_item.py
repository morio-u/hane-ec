from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(
        Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sku_id = Column(Integer, ForeignKey("skus.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    cart = relationship("Cart", back_populates="cart_items")
    sku = relationship("Sku")
