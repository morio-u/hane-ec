from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )  # If user is logged in, link
    session_token = Column(
        String(255), nullable=True, index=True
    )  # For users who are not logged in
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", back_populates="carts")
    cart_items = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )
