from typing import Optional
import uuid
from sqlalchemy.orm import Session, joinedload
from app.models import Cart, CartItem, Sku, User

def get_cart_query(db: Session, user: Optional[User] = None, session_token: Optional[str] = None) -> Optional[Cart]:
    """
    Helper function to retrieve the cart query filtered by either user ID or session token.
    Returns a query object that can be further modified.
    """
    cart_query = db.query(Cart)

    if user and user.id:
        cart_query = cart_query.filter(Cart.user_id == user.id)
    elif session_token:
        cart_query = cart_query.filter(Cart.session_token == session_token)
    else:
        return None  # No valid user or session token, return None

    return cart_query

def get_user_cart(db: Session, user: Optional[User] = None, session_token: Optional[str] = None) -> Optional[Cart]:
    """
    Retrieve the cart information for the user.
    - Filters by `user_id` if the user is provided.
    - If `session_token` is provided, filters by the session token.
    - Returns `None` if neither a valid user nor session token is provided.
    """
    cart_query = get_cart_query(db, user, session_token)

    if cart_query is None:
        return None

    cart = cart_query.first()

    return cart

def get_user_cart_with_items_and_skus(db: Session, user: Optional[User] = None, session_token: Optional[str] = None) -> Optional[Cart]:
    """
    Retrieves the user's cart along with its items and associated SKU details.
    If no cart is found for the given user or session token, None is returned.

    Parameters:
    - db: The database session.
    - user: The user whose cart is to be fetched. If provided, it filters the cart by user ID.
    - session_token: The session token used to identify the cart. If provided, it filters the cart by session token.

    Returns:
    - The user's cart with related cart items and SKU information, or None if no matching cart is found.
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
    Generate a new session token and return it.
    """
    return str(uuid.uuid4())