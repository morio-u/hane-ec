import json
import uuid
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, HTTPException, Request, Response, Cookie, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
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
    user=Depends(get_current_user)
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax
    cart_query = db.query(Cart)
    if user and user.id:
        cart_query = cart_query.filter(Cart.user_id == user.id)
    elif session_token:
        cart_query = cart_query.filter(Cart.session_token == session_token)
    else:
        session_token = str(uuid.uuid4())
        cart_query = cart_query.filter(Cart.session_token == session_token)
    cart = (
        cart_query
        .options(
            joinedload(Cart.cart_items)
            .joinedload(CartItem.sku)
            .joinedload(Sku.product)
        )
        .first()
    )

    cart_summary = []
    subtotal_amount = 0
    if cart:
        for item in cart.cart_items:
            cart_summary.append({
                "sku_id": item.sku.id,
                "sku": item.sku.barcode,
                "name": item.sku.product.name,
                "price": item.sku.product.price_excluding_tax,
                "quantity": item.quantity,
                "total": item.sku.product.price_excluding_tax * item.quantity,
            })
        subtotal_amount = sum(
            item.sku.product.price_excluding_tax * item.quantity
            for item in cart.cart_items
        )

    response = templates.TemplateResponse(
        "cart.html",
        {"request": request, "user": user, "cart_summary": cart_summary, "subtotal_amount": subtotal_amount}
    )
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS
    )
    return response

@router.post("/add")
def add_to_cart(
    response: Response,
    sku_id: int = Form(...),
    quantity: int = Form(...),
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax
    skus = db.query(Sku).filter(Sku.id == sku_id).all()
    if not skus:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_query = db.query(Cart)
    if user and user.id:
        cart_query = cart_query.filter(Cart.user_id == user.id)
    elif session_token:
        cart_query = cart_query.filter(Cart.session_token == session_token)
    else:
        session_token = str(uuid.uuid4())
        cart_query = cart_query.filter(Cart.session_token == session_token)
    cart = cart_query.first()

    if not cart:
        try:
            cart = Cart(
                user_id = user.id if user else None,
                session_token = session_token
            )
            db.add(cart)
            db.commit()
            db.refresh(cart)
        except Exception as e:
            raise e

    cart_item = db.query(CartItem).filter(CartItem.cart_id == Cart.id, CartItem.sku_id == sku_id).first()
    try:
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id = cart.id,
                sku_id = sku_id,
                quantity = quantity
            )
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
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS
    )
    return response

@router.post("/remove/{sku_id}")
def remove_from_cart(
    response: Response,
    sku_id: int,
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax
    cart_query = db.query(Cart)
    if user and user.id:
        cart_query = cart_query.filter(Cart.user_id == user.id)
    elif session_token:
        cart_query = cart_query.filter(Cart.session_token == session_token)
    else:
        session_token = str(uuid.uuid4())
        cart_query = cart_query.filter(Cart.session_token == session_token)

    cart = cart_query.first()
    if not cart:
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
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS
    )
    return response

@router.post("/update/{product_id}")
def update_cart(
    request: Request,
    response: Response,
    product_id: int,
    quantity: int = Form(...)
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax
    cart_cookie = request.cookies.get("cart")
    if cart_cookie:
        try:
            cart = json.loads(cart_cookie)
        except json.JSONDecodeError:
            cart = {}
    else:
        cart = {}

    pid = str(product_id)
    if pid in cart:
        cart[pid]["quantity"] = quantity
        cart[pid]["total"] = cart[pid]["quantity"] * cart[pid]["price"]

    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie(
        key="cart",
        value=json.dumps(cart),
        httponly=True,
        samesite="lax"
    )
    return response