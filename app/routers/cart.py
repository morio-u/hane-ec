from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Request, Response, Cookie, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.crud.cart import (
    get_user_cart,
    get_user_cart_with_items_and_skus,
    generate_session_token,
)
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models import Cart, CartItem, Sku

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("")
def view_cart(
    request: Request,
    response: Response,
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax
    if session_token is None:
        session_token = generate_session_token()

    # Retrieves the current user's cart with cart_items and skus.
    # Returns None if no matching cart is found.
    cart = get_user_cart_with_items_and_skus(db, user, session_token)

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_summary = []
    subtotal_amount = 0
    if cart:
        for cart_item in sorted(cart.cart_items, key=lambda cart_item: cart_item.id):
            # Organize cart data for display on the screen
            cart_summary.append(
                {
                    "sku_id": cart_item.sku.id,
                    "sku": cart_item.sku.barcode,
                    "name": cart_item.sku.product.name,
                    "price": cart_item.sku.product.price_excluding_tax,
                    "quantity": cart_item.quantity,
                    "total": cart_item.sku.product.price_excluding_tax * cart_item.quantity,
                }
            )
        subtotal_amount = sum(
            cart_item.sku.product.price_excluding_tax * cart_item.quantity
            for cart_item in cart.cart_items
        )

    response = templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "user": user,
            "cart_summary": cart_summary,
            "subtotal_amount": subtotal_amount,
        },
    )
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS,
    )
    return response


@router.post("/add")
def add_to_cart(
    response: Response,
    sku_id: int = Form(...),
    quantity: int = Form(...),
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax
    skus = db.query(Sku).filter(Sku.id == sku_id).all()
    if not skus:
        raise HTTPException(status_code=404, detail="Product not found")

    if session_token is None:
        session_token = generate_session_token()

    # Retrieve the cart information for the specified user.
    # Returns None if no matching cart is found.
    cart = get_user_cart(db, user, session_token)

    if cart is None:
        try:
            cart = Cart(user_id=user.id if user else None, session_token=session_token)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        except Exception as e:
            raise e

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.sku_id == sku_id)
        .first()
    )

    try:
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, sku_id=sku_id, quantity=quantity)
            db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
    except Exception as e:
        raise e

    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS,
    )
    return response


@router.post("/update/{sku_id}")
def update_cart(
    response: Response,
    sku_id: int,
    quantity: int = Form(...),
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax
    if session_token is None:
        session_token = generate_session_token()

    # Retrieve the cart information for the specified user.
    # Returns None if no matching cart is found.
    cart = get_user_cart(db, user, session_token)

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.sku_id == sku_id)
        .first()
    )

    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    try:
        if cart_item:
            cart_item.quantity = quantity
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
    except Exception as e:
        raise e

    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS,
    )
    return response


@router.post("/remove/{sku_id}")
def remove_from_cart(
    response: Response,
    sku_id: int,
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax
    if session_token is None:
        session_token = generate_session_token()

    # Retrieve the cart information for the specified user.
    # Returns None if no matching cart is found.
    cart = get_user_cart(db, user, session_token)

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_items_to_remove = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.sku_id == sku_id)
        .all()
    )

    if not cart_items_to_remove:
        raise HTTPException(status_code=404, detail="Cart items not found")

    try:
        for item in cart_items_to_remove:
            db.delete(item)
        db.commit()
    except Exception as e:
        raise e

    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS,
    )
    return response
