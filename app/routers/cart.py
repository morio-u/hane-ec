from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Request, Response, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.crud.cart import (
    create_or_increment_cart_item,
    get_or_create_cart,
    get_subtotal_amount,
    get_user_cart,
    get_user_cart_with_items_and_skus,
    make_cart_summary,
    remove_cart_item,
    update_cart_item_quantity,
)
from app.crud.sku import get_sku_by_id
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.session import get_or_create_session_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("")
def view_cart(
    request: Request,
    response: Response,
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        # Note: Intentionally not raising an error when cart is None.
        # The template will handle empty or missing cart gracefully.

        # Retrieves the current user's cart with cart_items and skus.
        # Returns None if no matching cart is found.
        cart = get_user_cart_with_items_and_skus(db, user, session_token)

        # Convert cart items into a summary format for display.
        cart_summary = make_cart_summary(cart)

        # Calculate the subtotal amount of all items in the cart.
        subtotal_amount = get_subtotal_amount(cart)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

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
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        # Retrieve a single SKU object by its unique ID.
        sku = get_sku_by_id(sku_id, db)
        if sku is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # Retrieve the cart for the specified user or session.
        # If no cart exists, create and retrieve a new one.
        cart = get_or_create_cart(db, user, session_token)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        # Create a new cart item if it doesn't exist, or increment the quantity if it does.
        # Returns the updated or newly created CartItem.
        cart_item = create_or_increment_cart_item(cart.id, sku_id, quantity, db)
        if not cart_item:
            raise HTTPException(status_code=404, detail="CartItem not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

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
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        # Retrieve a single SKU object by its unique ID.
        sku = get_sku_by_id(sku_id, db)
        if sku is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # Retrieve the cart information for the specified user.
        # Returns None if no matching cart is found.
        cart = get_user_cart(db, user, session_token)
        if cart is None:
            raise HTTPException(status_code=404, detail="Cart not found")

        # Update the quantity of an existing cart item.
        # Returns the updated CartItem.
        cart_item = update_cart_item_quantity(cart.id, sku_id, quantity, db)
        if not cart_item:
            raise HTTPException(status_code=404, detail="CartItem not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

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
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        # Retrieve a single SKU object by its unique ID.
        sku = get_sku_by_id(sku_id, db)
        if sku is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # Retrieve the cart information for the specified user.
        # Returns None if no matching cart is found.
        cart = get_user_cart(db, user, session_token)
        if cart is None:
            raise HTTPException(status_code=404, detail="Cart not found")

        # Delete a cart item by cart ID and SKU ID.
        remove_cart_item(cart.id, sku_id, db)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS,
    )
    return response
