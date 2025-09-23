import re
from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from sqlalchemy import func

def get_user_by_email(db: Session, input_email: str) -> Optional[User]:
    """
    Retrieves a user from the database by their email address (case-insensitive).

    Parameters:
        db (Session): The database session.
        input_email (str): The email address to search for.

    Returns:
        Optional[User]: The user if found, otherwise None.
    """
    return db.query(User).filter(func.lower(User.email) == input_email.lower()).first()

def clean_phone_number(phone_number: str) -> str:
    """
    Removes all non-numeric characters from a phone number.

    Parameters:
        phone_number (str): The input phone number string.

    Returns:
        str: A cleaned phone number containing only digits.
    """
    # Regular expression to remove non-numeric characters
    return re.sub(r'\D', '', phone_number)

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticates a user by verifying their email and password.

    Parameters:
        db (Session): The database session.
        email (str): The user's email address.
        password (str): The plaintext password to verify.

    Returns:
        Optional[User]: The authenticated user if credentials are valid, otherwise None.
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
        is_send_newsletter: bool
    ):
    """
    Creates and saves a new user in the database.

    Parameters:
        db (Session): The database session.
        last_name (str): The user's last name.
        first_name (str): The user's first name.
        gender (int): The user's gender identifier.
        phone_number (str): The user's phone number.
        email (str): The user's email address.
        password (str): The user's plaintext password.
        is_send_newsletter (bool): Whether the user opts in to receive newsletters.

    Returns:
        User: The newly created user.
    
    Raises:
        Exception: If the database operation fails.
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