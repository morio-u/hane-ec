from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.admin.admin_user import AdminUser


def get_admin_user_by_email(db: Session, input_email: str) -> Optional[AdminUser]:
    """
    Retrieves an admin user by email address (case-insensitive).

    Parameters:
        db (Session): The database session.
        input_email (str): The email address to search for.

    Returns:
        Optional[AdminUser]: The admin user if found, otherwise None.
    """
    return (
        db.query(AdminUser)
        .filter(func.lower(AdminUser.email) == input_email.lower())
        .first()
    )


def authenticate_admin_user(
    db: Session, email: str, password: str
) -> Optional[AdminUser]:
    """
    Authenticates an admin user by verifying their email and password.

    Parameters:
        db (Session): The database session.
        email (str): The admin user's email address.
        password (str): The plaintext password to verify.

    Returns:
        Optional[AdminUser]: The authenticated admin user if credentials are valid, otherwise None.
    """
    user_from_db = get_admin_user_by_email(db, email)
    if not user_from_db:
        return None
    if not verify_password(password, user_from_db.password):
        return None
    return user_from_db


def create_admin_user(
    db: Session,
    last_name: str,
    first_name: str,
    email: str,
    password: str,
    role_id: int,
) -> AdminUser:
    """
    Creates and saves a new admin user in the database.

    Parameters:
        db (Session): The database session.
        last_name (str): The admin user's last name.
        first_name (str): The admin user's first name.
        email (str): The admin user's email address.
        password (str): The admin user's plaintext password.
        role_id (int): The role identifier for the admin user.

    Returns:
        AdminUser: The newly created admin user.

    Raises:
        Exception: If the database operation fails.
    """
    # Hash the password and remove non-numeric characters from the phone number
    hashed_pw = get_password_hash(password)

    new_user = AdminUser(
        last_name=last_name,
        first_name=first_name,
        email=email,
        password=hashed_pw,
        role_id=role_id,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise e

    return new_user
