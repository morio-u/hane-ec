from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    label = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    street_line1 = Column(String(100), nullable=False)
    street_line2 = Column(String(100), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(10), nullable=False)
    phone_number = Column(String(15), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", back_populates="addresses")
