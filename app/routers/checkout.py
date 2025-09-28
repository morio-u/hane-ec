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
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models import (
    Order,
    OrderItem,
    Payment,
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
    order_status = OrderStatusEnum.confirmed
    shipping_status = ShippingStatusEnum.preparing
    payment_status = PaymentStatusEnum.unpaid

    new_order = Order(
        user_id=user.id if user and user.id else None,
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

    # TODO: get target tax, use sample values temporally
    transaction_token = "0123456789"
    tax_rate = Decimal("0.1")

    new_order_items = []
    if new_order and new_order.id:
        for cart_item in sorted(cart.cart_items, key=lambda cart_item: cart_item.id):
            # TODO: get target tax, use sample values temporally
            # TODO: Item_price is not necessarily the list price
            item_price = cart_item.sku.product.price_excluding_tax
            quantity = cart_item.quantity
            tax_amount = tax_rate * item_price * quantity

            new_order_items.append(
                OrderItem(
                    order_id=new_order.id,
                    sku_id=cart_item.sku.id,
                    product_name=cart_item.sku.product.name,
                    item_price=item_price,
                    quantity=quantity,
                    item_total_amount=cart_item.sku.product.price_excluding_tax
                    * cart_item.quantity,
                    tax_rate=tax_rate,
                    tax_amount=tax_amount 
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

        new_payment = Payment(
            user_id=user.id if user and user.id else None,
            order_id=new_order.id,
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
        db.delete(cart)
        db.commit()
    return templates.TemplateResponse(
        "checkout_complete.html", {"request": request, "user": user, "order_id": new_order.id}
    )
