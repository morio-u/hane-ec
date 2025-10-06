from decimal import Decimal
from typing import Any, List, Dict, Optional
from sqlalchemy.orm import Session, joinedload
from app.core.exception import RedirectHomeException
from app.crud.sku import get_sku_by_id
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
    Retrieves the user's cart based on the user or session token.

    Parameters:
        db (Session): The database session.
        user (Optional[User]): The user associated with the cart.
        session_token (Optional[str]): The session token for guest users.

    Returns:
        Optional[Cart]: The Cart object if found, otherwise None.
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


def make_cart_summary(cart: Cart) -> List[Dict[str, Any]]:
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
                "product_id": cart_item.sku.product.id,
                "quantity": cart_item.quantity,
                "total": cart_item.sku.product.price_excluding_tax * cart_item.quantity,
            }
        )

    return cart_summary


def get_subtotal_amount(cart: Cart) -> Decimal:
    """
    Calculate the subtotal amount of all items in the cart.

    Args:
        cart (Cart): The Cart model instance.

    Returns:
        Decimal: The subtotal (excluding tax).
    """
    if not cart or not cart.cart_items:
        return 0.0

    return sum(
        cart_item.sku.product.price_excluding_tax * cart_item.quantity
        for cart_item in cart.cart_items
    )


def get_cart_item_by_sku(cart_id: int, sku_id: int, db: Session) -> Optional[CartItem]:
    """
    Retrieve a specific cart item by cart ID and SKU ID.

    Args:
        db (Session): The database session.
        cart_id (int): The ID of the cart.
        sku_id (int): The ID of the SKU.

    Returns:
        Optional[CartItem]: The matching cart item if found, otherwise None.
    """
    if cart_id is None or sku_id is None:
        return None

    return (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart_id, CartItem.sku_id == sku_id)
        .first()
    )


def get_or_create_cart(
    db: Session, user: Optional[User] = None, session_token: Optional[str] = None
) -> Cart:
    """
    Retrieve the cart for the specified user or session.
    If no cart exists, create a new one.

    Args:
        db (Session): SQLAlchemy database session.
        user (Optional[User]): The user object, if logged in.
        session_token (Optional[str]): A unique token for guest users.

    Returns:
        Cart: The retrieved or newly created cart.
    """
    cart = get_user_cart(db, user, session_token)

    if cart is None:
        try:
            cart = Cart(user_id=user.id if user else None, session_token=session_token)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        except Exception as e:
            db.rollback()
            raise e

    return cart


def create_or_increment_cart_item(
    cart_id: int, sku_id: int, quantity: int, db: Session
) -> CartItem:
    """
    Create a new cart item or update the quantity of an existing one.

    Args:
        cart_id (int): The cart ID.
        sku_id (int): The SKU ID.
        quantity (int): The quantity to add to the cart item.
        db (Session): The database session.

    Returns:
        CartItem: The created or updated cart item.
    """
    cart_item = get_cart_item_by_sku(cart_id, sku_id, db)

    try:
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart_id, sku_id=sku_id, quantity=quantity)
            db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
    except Exception as e:
        db.rollback()
        raise e

    return cart_item


def update_cart_item_quantity(
    cart_id: int, sku_id: int, quantity: int, db: Session
) -> CartItem:
    """
    Update the quantity of an existing cart item.

    Args:
        cart_id (int): The ID of the cart that contains the item.
        sku_id (int): The ID of the SKU to be updated.
        quantity (int): The new quantity to set.
        db (Session): The database session.

    Returns:
        CartItem: The updated cart item.

    Raises:
        RedirectHomeException or ValueError: If the cart item does not exist.
    """
    cart_item = get_cart_item_by_sku(cart_id, sku_id, db)

    if cart_item is None:
        raise RedirectHomeException("Cart item not found")

    cart_item.quantity = quantity
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


def remove_cart_item(cart_id: int, sku_id: int, db: Session) -> None:
    """
    Delete a cart item by cart ID and SKU ID.

    Args:
        cart_id (int): The ID of the cart that contains the item.
        sku_id (int): The ID of the SKU to be removed.
        db (Session): The database session.

    Raises:
        RedirectHomeException: If the cart item does not exist.
    """
    cart_item_to_remove = get_cart_item_by_sku(cart_id, sku_id, db)

    if not cart_item_to_remove:
        raise RedirectHomeException("Cart item not found")

    try:
        db.delete(cart_item_to_remove)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def process_view_cart(user: Optional[User], session_token: str, db: Session):
    """
    Retrieve and prepare the user's cart data for display, including cart summary and subtotal.

    This function fetches the current user's cart along with related cart items and SKU details.
    If no cart exists, it returns empty summary and subtotal gracefully without raising an error.

    Args:
        user (Optional[User]): The authenticated user, or None for guest users.
        session_token (str): The session token used to identify the guest cart.
        db (Session): The SQLAlchemy database session.

    Returns:
        Tuple[List[CartItemSummary], Decimal]:
            - cart_summary: A list of summarized cart items for display.
            - subtotal_amount: The total price of all items in the cart.

    Note:
        If the cart does not exist, the return values will represent an empty cart.
        It's expected that the calling template handles this case gracefully.
    """
    # Note: Intentionally not raising an error when cart is None.
    # The template will handle empty or missing cart gracefully.

    # Retrieves the current user's cart with cart_items and skus.
    # Returns None if no matching cart is found.
    cart = get_user_cart_with_items_and_skus(db, user, session_token)

    # Convert cart items into a summary format for display.
    cart_summary = make_cart_summary(cart)

    # Calculate the subtotal amount of all items in the cart.
    subtotal_amount = get_subtotal_amount(cart)

    return cart_summary, subtotal_amount


def process_add_to_cart(
    sku_id: int, quantity: int, user: Optional[User], session_token: str, db: Session
):
    """
    Add a SKU to the user's cart, or increment the quantity if it already exists.

    Args:
        sku_id (int): The ID of the SKU to add to the cart.
        quantity (int): The quantity to add.
        user (User or None): The authenticated user, or None for guest users.
        session_token (str): The session token for identifying guest users.
        db (Session): The database session.

    Raises:
        RedirectHomeException: If the SKU does not exist, the cart could not be retrieved or created,
                       or the cart item could not be created or updated.
    """
    # Retrieve a single SKU object by its unique ID.
    sku = get_sku_by_id(sku_id, db)
    if sku is None:
        raise RedirectHomeException("Product not found")

    # Retrieve the cart for the specified user or session.
    # If no cart exists, create and retrieve a new one.
    cart = get_or_create_cart(db, user, session_token)
    if not cart:
        raise RedirectHomeException("Cart not found")

    # Create a new cart item if it doesn't exist, or increment the quantity if it does.
    # Returns the updated or newly created CartItem.
    cart_item = create_or_increment_cart_item(cart.id, sku_id, quantity, db)
    if not cart_item:
        raise RedirectHomeException("CartItem not found")


def process_update_cart(
    sku_id: int, quantity: int, user: Optional[User], session_token: str, db: Session
):
    """
    Update the quantity of an existing cart item in the user's cart.

    Args:
        sku_id (int): The ID of the SKU to update.
        quantity (int): The new quantity to set.
        user (User or None): The authenticated user, or None for guest users.
        session_token (str): The session token for identifying guest users.
        db (Session): The database session.

    Raises:
        RedirectHomeException: If the SKU does not exist, the cart is not found,
                       or the cart item could not be updated.
    """
    # Retrieve a single SKU object by its unique ID.
    sku = get_sku_by_id(sku_id, db)
    if sku is None:
        raise RedirectHomeException("Product not found")

    # Retrieve the cart information for the specified user.
    # Returns None if no matching cart is found.
    cart = get_user_cart(db, user, session_token)
    if cart is None:
        raise RedirectHomeException("Cart not found")

    # Update the quantity of an existing cart item.
    # Returns the updated CartItem.
    cart_item = update_cart_item_quantity(cart.id, sku_id, quantity, db)
    if not cart_item:
        raise RedirectHomeException("CartItem not found")


def process_remove_from_cart(
    sku_id: int, user: Optional[User], session_token: str, db: Session
):
    """
    Remove a SKU from the user's cart.

    Args:
        sku_id (int): The ID of the SKU to remove.
        user (User or None): The authenticated user, or None for guest users.
        session_token (str): The session token for identifying guest users.
        db (Session): The database session.

    Raises:
        RedirectHomeException: If the SKU does not exist or the cart is not found.
    """
    # Retrieve a single SKU object by its unique ID.
    sku = get_sku_by_id(sku_id, db)
    if sku is None:
        raise RedirectHomeException("Product not found")

    # Retrieve the cart information for the specified user.
    # Returns None if no matching cart is found.
    cart = get_user_cart(db, user, session_token)
    if cart is None:
        raise RedirectHomeException("Cart not found")

    # Delete a cart item by cart ID and SKU ID.
    remove_cart_item(cart.id, sku_id, db)
