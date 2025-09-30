from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Request, Cookie, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.session import get_or_create_session_token
from app.crud.cart import (
    get_subtotal_amount,
    get_user_cart_with_items_and_skus,
)
from app.crud.checkout import (
    create_new_order,
    create_new_order_item,
    create_new_payment,
)
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models import (
    OrderStatusEnum,
    PaymentStatusEnum,
    ShippingStatusEnum,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("", response_class=HTMLResponse)
def view_checkout_form(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "checkout_form.html",
        {"request": request, "user": user},
    )


@router.post("/confirm", response_class=HTMLResponse)
def checkout_confirm(
    request: Request,
    shipping_last_name: str = Form(...),
    shipping_first_name: str = Form(...),
    shipping_address_line1: str = Form(...),
    shipping_address_line2: str = Form(""),
    shipping_city: str = Form(...),
    shipping_state: str = Form(...),
    shipping_zip: str = Form(...),
    shipping_phone_number: str = Form(...),
    shipping_method: str = Form(...),
    payment_method: str = Form(...),
    card_number: str = Form(...),
    card_name: str = Form(...),
    card_cvv: str = Form(...),
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation
    session_token = get_or_create_session_token(session_token)

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

    order = {
        "shipping_last_name": shipping_last_name,
        "shipping_first_name": shipping_first_name,
        "shipping_address_line1": shipping_address_line1,
        "shipping_address_line2": shipping_address_line2,
        "shipping_city": shipping_city,
        "shipping_state": shipping_state,
        "shipping_zip": shipping_zip,
        "shipping_phone_number": shipping_phone_number,
        "shipping_method": shipping_method,
        "payment_method": payment_method,
        "card_number": card_number,
        "card_name": card_name,
        "card_cvv": card_cvv,
        "subtotal_amount": subtotal_amount,
        "shipping_fee": shipping_fee,
        "tax": tax,
        "total": total,
    }

    return templates.TemplateResponse(
        "checkout_confirm.html", {"request": request, "order": order, "user": user}
    )


@router.post("/complete", name="checkout_complete", response_class=HTMLResponse)
def checkout_complete(
    request: Request,
    shipping_last_name: str = Form(...),
    shipping_first_name: str = Form(...),
    shipping_address_line1: str = Form(...),
    shipping_address_line2: str = Form(""),
    shipping_city: str = Form(...),
    shipping_state: str = Form(...),
    shipping_zip: str = Form(...),
    shipping_phone_number: str = Form(...),
    shipping_method: str = Form(...),
    payment_method: str = Form(...),
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation
    session_token = get_or_create_session_token(session_token)

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
        shipping_last_name,
        shipping_first_name,
        shipping_address_line1,
        shipping_city,
        shipping_state,
        shipping_zip,
        shipping_phone_number,
        subtotal_amount,
        tax_amount,
        shipping_fee,
        payment_processing_fee,
        total_amount,
        shipping_method,
        OrderStatusEnum.confirmed,
        ShippingStatusEnum.preparing,
        PaymentStatusEnum.unpaid,
        shipping_address_line2,
        user.id if user and user.id else None,
    )

    # TODO: get target tax, use sample values temporally
    transaction_token = "0123456789"

    if new_order.id:
        try:
            # Create OrderItem records in the database based on the items in the given cart
            # and associate them with the specified order ID.
            new_order_items = create_new_order_item(new_order.id, cart, db)
            # The returned new_order_items is assigned but not used here.

            # Create a new payment record and persist it in the database.
            new_payment = create_new_payment(
                new_order.id,
                payment_method,
                PaymentStatusEnum.unpaid,
                transaction_token,
                db,
                user.id if user and user.id else None,
            )
            # The returned new_payment is assigned but not used here.

            db.delete(cart)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
    else:
        raise HTTPException(status_code=404, detail="Order not found")

    return templates.TemplateResponse(
        "checkout_complete.html",
        {"request": request, "user": user, "order_id": new_order.id},
    )
