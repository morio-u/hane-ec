from typing import Optional
import uuid
from sqlalchemy.orm import Session, joinedload
from app.models import Cart, CartItem, Sku, User

def get_cart_query(db: Session, user: Optional[User] = None, session_token: Optional[str] = None) -> Optional[Cart]:
    """
    Builds a base query to retrieve a cart filtered by user ID or session token.

    Parameters:
        db (Session): The database session.
        user (Optional[User]): The user associated with the cart.
        session_token (Optional[str]): The session token for guest users.

    Returns:
        Optional[Query]: A SQLAlchemy query object for the cart, or None if neither user nor session token is provided.
    """
    cart_query = db.query(Cart)

    if session_token:
        cart_query = cart_query.filter(Cart.session_token == session_token)
    elif user and user.id:
        cart_query = cart_query.filter(Cart.user_id == user.id)
    else:
        return None  # No valid user or session token, return None

    return cart_query

def get_user_cart(db: Session, user: Optional[User] = None, session_token: Optional[str] = None) -> Optional[Cart]:
    """
    Builds a base query to retrieve a cart filtered by user ID or session token.

    Parameters:
        db (Session): The database session.
        user (Optional[User]): The user associated with the cart.
        session_token (Optional[str]): The session token for guest users.

    Returns:
        Optional[Query]: A SQLAlchemy query object for the cart, or None if neither user nor session token is provided.
    """
    cart_query = get_cart_query(db, user, session_token)

    if cart_query is None:
        return None

    cart = cart_query.first()

    return cart

def get_user_cart_with_items_and_skus(db: Session, user: Optional[User] = None, session_token: Optional[str] = None) -> Optional[Cart]:
    """
    Retrieves a cart along with its items, SKUs, and associated products.

    Parameters:
        db (Session): The database session.
        user (Optional[User]): The user associated with the cart.
        session_token (Optional[str]): The session token for guest users.

    Returns:
        Optional[Cart]: The cart with related items and product details, or None if not found.
    """
    cart_query = get_cart_query(db, user, session_token)

    if cart_query is None:
        return None

    cart = (
        cart_query
        .options(
            joinedload(Cart.cart_items)
            .joinedload(CartItem.sku)
            .joinedload(Sku.product)
        )
        .first()
    )

    return cart

def generate_session_token() -> str:
    """
    Generates a new unique session token.

    Returns:
        str: A UUID-based session token as a string.
    """
    return str(uuid.uuid4())