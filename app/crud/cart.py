from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models import Cart, CartItem, Sku, User


def get_cart_query(
    db: Session, user: Optional[User] = None, session_token: Optional[str] = None
) -> Optional[Cart]:
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


def get_user_cart(
    db: Session, user: Optional[User] = None, session_token: Optional[str] = None
) -> Optional[Cart]:
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


def get_user_cart_with_items_and_skus(
    db: Session, user: Optional[User] = None, session_token: Optional[str] = None
) -> Optional[Cart]:
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

    cart = cart_query.options(
        joinedload(Cart.cart_items).joinedload(CartItem.sku).joinedload(Sku.product)
    ).first()

    return cart


def make_cart_summary(cart: Cart) -> List[dict]:
    """
    Convert cart items into a summary format for display.

    Args:
        cart (Cart): The Cart model instance containing cart_items.

    Returns:
        List[dict]: A list of dictionaries summarizing each cart item for display.
    """
    cart_summary = []

    if not cart or not cart.cart_items:
        return cart_summary

    for cart_item in sorted(cart.cart_items, key=lambda cart_item: cart_item.id):
        cart_summary.append(
            {
                "sku_id": cart_item.sku.id,
                "sku": cart_item.sku.barcode,
                "name": cart_item.sku.product.name,
                "price": cart_item.sku.product.price_excluding_tax,
                "quantity": cart_item.quantity,
                "total": cart_item.sku.product.price_excluding_tax
                * cart_item.quantity,
            }
        )

    return cart_summary


def get_subtotal_amount(cart: Cart) -> float:
    """
    Calculate the subtotal amount of all items in the cart.

    Args:
        cart (Cart): The Cart model instance.

    Returns:
        float: The subtotal (excluding tax).
    """
    if not cart or not cart.cart_items:
        return 0.0

    return sum(
        cart_item.sku.product.price_excluding_tax * cart_item.quantity
        for cart_item in cart.cart_items
    )
