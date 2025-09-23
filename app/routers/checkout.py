from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Request, Cookie, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.crud.cart import (
    get_user_cart_with_items_and_skus,
    generate_session_token,
)
from app.database import get_db
from app.dependencies.auth import get_current_user

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
    if session_token is None:
        session_token = generate_session_token()

    # Retrieves the current user's cart with cart_items and skus.
    # Returns None if no matching cart is found.
    cart = get_user_cart_with_items_and_skus(db, user, session_token)

    subtotal_amount = 0
    if cart:
        subtotal_amount = sum(
            cart_item.sku.product.price_excluding_tax * cart_item.quantity
            for cart_item in cart.cart_items
        )
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

    # TODO: get target tax, use sample values temporally
    # tax = get_tax()
    tax_per = Decimal("0.1")
    tax = subtotal_amount * tax_per
    shipping_cost = Decimal("20.00")
    total = subtotal_amount + shipping_cost + tax

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
        "shipping_cost": shipping_cost,
        "tax": tax,
        "total": total,
    }

    return templates.TemplateResponse(
        "checkout_confirm.html", {"request": request, "order": order, "user": user}
    )


@router.post("/complete", name="checkout_complete", response_class=HTMLResponse)
def checkout_complete(
    request: Request,
    user=Depends(get_current_user),
):

    return templates.TemplateResponse(
        "checkout_complete.html", {"request": request, "user": user}
    )
