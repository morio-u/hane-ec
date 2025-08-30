from sqlalchemy import Column, BigInteger, String, SmallInteger, TIMESTAMP, func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    gender = Column(SmallInteger, nullable=False)
    phone_number = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(SmallInteger, nullable=False, default=0)
    status = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())