import re
from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from sqlalchemy import func

def get_user_by_email(db: Session, input_email: str) -> Optional[User]:
    return db.query(User).filter(func.lower(User.email) == input_email.lower()).first()

def clean_phone_number(phone_number: str) -> str:
    # Regular expression to remove non-numeric characters
    return re.sub(r'\D', '', phone_number)

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Asynchronous user authentication function
    Ensure it can be called with await even when replaced in the database
    """
    user_from_db = get_user_by_email(db, email)
    if not user_from_db:
        return None
    if not verify_password(password, user_from_db.password):
        return None
    return user_from_db

def create_user(
        db: Session,
        last_name: str,
        first_name: str,
        gender: int,
        phone_number: str,
        email: str,
        password: str,
        is_send_newsletter: bool,
        middle_name: Optional[str] = None
    ):
    """
    Create a new user and save it to the database
    """
    # Hash the password and remove non-numeric characters from the phone number
    hashed_pw = get_password_hash(password)
    cleaned_pn = clean_phone_number(phone_number)

    new_user = User(
        last_name=last_name,
        first_name=first_name,
        gender=gender,
        phone_number=cleaned_pn,
        email=email,
        password=hashed_pw,
        is_send_newsletter=is_send_newsletter
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise e

    return new_user