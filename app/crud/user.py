from sqlalchemy.orm import Session
from typing import Optional
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from sqlalchemy import func
import re

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.name == username).first()

def get_user_by_email(db: Session, input_email: str) -> Optional[User]:
    return db.query(User).filter(func.lower(User.email) == input_email.lower()).first()

def clean_phone_number(phone_number: str) -> str:
    # Regular expression to remove non-numeric characters
    return re.sub(r'\D', '', phone_number)

async def authenticate_user(db: Session, username: str, password: str):
    """
    Asynchronous user authentication function
    Ensure it can be called with await even when replaced in the database
    """
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_user(
        db: Session,
        last_name: str,
        first_name: str,
        gender: int,
        phone_number: str,
        email: str,
        password: str,
        is_send_newsletter: bool,
        middle_name: Optional[str] = None,
    ):
    """
    Create a new user and save it to the database
    """
    hashed_pw = get_password_hash(password)
    normalized_pn = clean_phone_number(phone_number)

    new_user = User(
        last_name=last_name,
        middle_name=middle_name,
        first_name=first_name,
        gender=gender,
        phone_number=normalized_pn,
        email=email,
        password=hashed_pw,
        is_send_newsletter=is_send_newsletter
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return last_name