from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.crud.cart import (
    get_subtotal_amount,
    get_user_cart_with_items_and_skus,
)
from app.crud.checkout import (
    create_new_order,
    create_new_order_item,
    create_new_payment,
    delete_cart,
)
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.session import get_or_create_session_token
from app.models.order import (
    OrderStatusEnum,
    PaymentStatusEnum,
    ShippingStatusEnum,
)
from app.models.user import User
from app.schemas.checkout import CheckoutConfirmForm, CheckoutCompleteForm

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("", response_class=HTMLResponse)
def view_checkout_form(
    request: Request, user: Optional[User] = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "checkout_form.html",
        {"request": request, "user": user},
    )


@router.post("/confirm", response_class=HTMLResponse)
def checkout_confirm(
    request: Request,
    form: CheckoutConfirmForm = Depends(CheckoutConfirmForm.as_form),
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    # TODO: Add validation

    # Retrieves the current user's cart with cart_items and skus.
    # Returns None if no matching cart is found.
    cart = get_user_cart_with_items_and_skus(db, user, session_token)

    if cart:
        # Calculate the subtotal amount of all items in the cart.
        subtotal_amount = get_subtotal_amount(cart)
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

    # TODO: get target tax, use sample values temporally
    # tax = get_tax()
    tax_per = Decimal("0.1")
    tax = subtotal_amount * tax_per
    shipping_fee = Decimal("20.00")
    total = subtotal_amount + shipping_fee + tax

    order = form.dict()
    order.update(
        {
            "subtotal_amount": subtotal_amount,
            "shipping_fee": shipping_fee,
            "tax": tax,
            "total": total,
        }
    )

    return templates.TemplateResponse(
        "checkout_confirm.html", {"request": request, "order": order, "user": user}
    )


@router.post("/complete", name="checkout_complete", response_class=HTMLResponse)
def checkout_complete(
    request: Request,
    form: CheckoutCompleteForm = Depends(CheckoutCompleteForm.as_form),
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    # TODO: Add validation

    # Retrieves the current user's cart with cart_items and skus.
    # Returns None if no matching cart is found.
    cart = get_user_cart_with_items_and_skus(db, user, session_token)

    if cart:
        # Calculate the subtotal amount of all items in the cart.
        subtotal_amount = get_subtotal_amount(cart)
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

    # TODO: get target tax, use sample values temporally
    # tax = get_tax()
    tax_per = Decimal("0.1")
    tax_amount = subtotal_amount * tax_per
    shipping_fee = Decimal("20.00")
    payment_processing_fee = Decimal("5.00")
    total_amount = subtotal_amount + shipping_fee + tax_amount

    new_order = create_new_order(
        db,
        form.shipping_last_name,
        form.shipping_first_name,
        form.shipping_address_line1,
        form.shipping_city,
        form.shipping_state,
        form.shipping_zip,
        form.shipping_phone_number,
        subtotal_amount,
        tax_amount,
        shipping_fee,
        payment_processing_fee,
        total_amount,
        form.shipping_method,
        OrderStatusEnum.confirmed,
        ShippingStatusEnum.preparing,
        PaymentStatusEnum.unpaid,
        form.shipping_address_line2,
        user.id if user and user.id else None,
    )

    # TODO: get target tax, use sample values temporally
    transaction_token = "0123456789"

    if new_order.id:
        try:
            # Create OrderItem records in the database based on the items in the given cart
            # and associate them with the specified order ID.
            new_order_items = create_new_order_item(new_order.id, cart, db)
            if not new_order_items:
                raise HTTPException(status_code=404, detail="Order not found")

            # Create a new payment record and persist it in the database.
            new_payment = create_new_payment(
                new_order.id,
                form.payment_method,
                PaymentStatusEnum.unpaid,
                transaction_token,
                db,
                user.id if user and user.id else None,
            )
            if not new_payment:
                raise HTTPException(status_code=404, detail="Order not found")

            # Deletes the specified cart from the database.
            delete_cart(cart, db)
        except Exception as e:
            db.rollback()
            raise e
    else:
        raise HTTPException(status_code=404, detail="Order not found")

    return templates.TemplateResponse(
        "checkout_complete.html",
        {"request": request, "user": user, "order_id": new_order.id},
    )
