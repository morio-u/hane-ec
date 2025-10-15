from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.shop import (
    Cart,
    Order,
    OrderItem,
    Payment,
    OrderStatusEnum,
    PaymentStatusEnum,
    ShippingStatusEnum,
)


def create_new_order(
    db: Session,
    shipping_first_name: str,
    shipping_last_name: str,
    shipping_address_line1: str,
    shipping_city: str,
    shipping_state: str,
    shipping_zip: str,
    shipping_phone_number: str,
    subtotal_amount: Decimal,
    tax_amount: Decimal,
    shipping_fee: Decimal,
    payment_processing_fee: Decimal,
    total_amount: Decimal,
    shipping_method: str,
    order_status: OrderStatusEnum,
    shipping_status: ShippingStatusEnum,
    payment_status: PaymentStatusEnum,
    shipping_address_line2: Optional[str] = None,
    user_id: Optional[int] = None,
) -> Order:
    """
    Create a new order and save it to the database.

    This function constructs an Order object with the provided shipping and payment
    information, associates it with a user if given, and persists it to the database.

    Args:
        db (Session): The SQLAlchemy database session.
        shipping_first_name (str): Recipient's first name.
        shipping_last_name (str): Recipient's last name.
        shipping_address_line1 (str): Primary shipping address.
        shipping_address_line2 (Optional[str]): Secondary shipping address (e.g. apartment or building).
        shipping_city (str): City of the shipping address.
        shipping_state (str): State or region of the shipping address.
        shipping_zip (str): ZIP or postal code of the shipping address.
        shipping_phone_number (str): Phone number for shipping contact.
        subtotal_amount (Decimal): Subtotal amount of the order before tax and fees.
        tax_amount (Decimal): Tax applied to the order.
        shipping_fee (Decimal): Fee for the selected shipping method.
        payment_processing_fee (Decimal): Fee charged for payment processing.
        total_amount (Decimal): Total cost of the order including all fees and taxes.
        shipping_method (str): The chosen shipping method (e.g., "standard", "express").
        order_status (OrderStatusEnum): Status of the order (e.g., "pending", "completed").
        shipping_status (ShippingStatusEnum): Current shipping status (e.g., "not_shipped", "shipped").
        payment_status (PaymentStatusEnum): Status of the payment (e.g., "unpaid", "paid").
        user_id (Optional[int]): ID of the user placing the order, if available.

    Returns:
        Order: The newly created Order object after being committed to the database.

    Raises:
        Exception: If any error occurs during the database transaction, it will be rolled back and re-raised.
    """
    new_order = Order(
        user_id=user_id,
        shipping_last_name=shipping_last_name,
        shipping_first_name=shipping_first_name,
        shipping_address_line1=shipping_address_line1,
        shipping_address_line2=shipping_address_line2,
        shipping_city=shipping_city,
        shipping_state=shipping_state,
        shipping_zip=shipping_zip,
        shipping_phone_number=shipping_phone_number,
        subtotal_amount=subtotal_amount,
        tax_amount=tax_amount,
        shipping_fee=shipping_fee,
        payment_processing_fee=payment_processing_fee,
        total_amount=total_amount,
        shipping_method=shipping_method,
        order_status=order_status,
        shipping_status=shipping_status,
        payment_status=payment_status,
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except Exception as e:
        db.rollback()
        raise e

    return new_order


def create_new_order_item(
    new_order_id: int, cart: Cart, db: Session
) -> List[OrderItem]:
    """
    Create OrderItem records in the database based on the items in the given cart
    and associate them with the specified order ID.

    Args:
        new_order_id (int): The ID of the existing order to link items to.
        cart (Cart): The cart containing items to be converted into order items.
        db (Session): SQLAlchemy database session for transaction handling.

    Returns:
        List[OrderItem]: A list of newly created OrderItem instances with updated fields
                         (including generated IDs) after committing to the database.

    Raises:
        Exception: Rolls back the transaction and re-raises any exceptions encountered during database operations.
    """
    # TODO: get target tax, use sample values temporally
    tax_rate = Decimal("0.1")

    new_order_items = []
    if new_order_id:
        for cart_item in sorted(cart.cart_items, key=lambda cart_item: cart_item.id):
            # TODO: get target tax, use sample values temporally
            # TODO: Item_price is not necessarily the list price
            item_price = cart_item.sku.product.price_excluding_tax
            quantity = cart_item.quantity
            tax_amount = tax_rate * item_price * quantity

            new_order_items.append(
                OrderItem(
                    order_id=new_order_id,
                    sku_id=cart_item.sku.id,
                    product_name=cart_item.sku.product.name,
                    item_price=item_price,
                    quantity=quantity,
                    item_total_amount=cart_item.sku.product.price_excluding_tax
                    * cart_item.quantity,
                    tax_rate=tax_rate,
                    tax_amount=tax_amount,
                )
            )

        try:
            db.add_all(new_order_items)
            db.commit()
            for new_order_item in new_order_items:
                db.refresh(new_order_item)
        except Exception as e:
            db.rollback()
            raise e

    return new_order_items


def create_new_payment(
    new_order_id: int,
    payment_method: str,
    payment_status: PaymentStatusEnum,
    transaction_token: str,
    db: Session,
    user_id: Optional[int] = None,
) -> Payment:
    """
    Create a new payment record and persist it in the database.

    Args:
        user_id (Optional[int]): ID of the user making the payment, or None for guest checkouts.
        new_order_id (int): ID of the order this payment is associated with.
        payment_method (str): Payment method used (e.g., 'credit_card', 'paypal').
        payment_status (PaymentStatusEnum): Initial status of the payment (e.g., 'pending', 'completed').
        transaction_token (str): Token or ID representing the transaction (from payment gateway).
        db (Session): SQLAlchemy database session.

    Returns:
        Payment: The newly created Payment object with generated fields (e.g., ID).

    Raises:
        Exception: Rolls back the transaction and re-raises the exception if any database error occurs.
    """
    new_payment = Payment(
        user_id=user_id,
        order_id=new_order_id,
        payment_method=payment_method,
        payment_status=payment_status,
        transaction_token=transaction_token,
    )

    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
    except Exception as e:
        db.rollback()
        raise e

    return new_payment


def delete_cart(cart: Cart, db: Session) -> None:
    """
    Deletes the specified cart from the database.

    Parameters:
        cart (Cart): The cart instance to be deleted.
        db (Session): The database session used to perform the operation.

    Returns:
        None: This function performs a side effect (deleting a cart) and does not return a value.

    Raises:
        Exception: If the deletion or commit fails, the transaction is rolled back and the exception is re-raised.
    """
    try:
        db.delete(cart)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
