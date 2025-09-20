import json
from fastapi import Request, Response, APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dependencies.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")

@router.get("")
def view_cart(
    request: Request,
    response: Response,
    user=Depends(get_current_user)
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

    subtotal_amount = 0
    for product in cart.values():
        subtotal_amount += product["total"]

    response = templates.TemplateResponse(
        "cart.html",
        {"request": request, "user": user, "cart": cart, "subtotal_amount": subtotal_amount}
    )
    response.set_cookie(
        key="cart",
        value=json.dumps(cart),
        httponly=True,
        samesite="lax"
    )
    return response

@router.post("/add/{product_id}")
def add_to_cart(
    request: Request,
    response: Response,
    product_id: int,
    quantity: int = Form(...),
    name: str = Form(...),
    price: float = Form(...)
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
        cart[pid]["quantity"] += quantity
        cart[pid]["total"] = cart[pid]["quantity"] * price
    else:
        cart[pid] = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "total": price * quantity
        }

    # Grand_total is calculated by "view_cart" function
    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie(
        key="cart",
        value=json.dumps(cart),
        httponly=True,
        samesite="lax"
    )
    return response

@router.post("/remove/{product_id}")
def remove_from_cart(
    request: Request,
    response: Response,
    product_id: int
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
        del cart[pid]

    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie(
        key="cart",
        value=json.dumps(cart),
        httponly=True,
        samesite="lax"
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