from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Depends ,Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.exception import RedirectHomeException
from app.crud.cart import process_add_to_cart
from app.crud.products import get_all_products, get_product_by_id, get_skus_by_id
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.session import (
    get_errors_from_session,
    get_or_create_session_token,
)
from app.models.user import User
from app.validators.products import validate_add_to_cart
from app.schemas.products import AddToCartForm
import logging

logger = logging.getLogger(__name__)


router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("", response_class=HTMLResponse)
def get_products(
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    try:
        # Retrieves all products from the database.
        products = get_all_products(db)
    except Exception as e:
        # For traceback
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return templates.TemplateResponse(
        "products.html", {"request": request, "products": products, "user": user}
    )


@router.get("/{product_id}", response_class=HTMLResponse)
def get_product_detail(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
    errors: Optional[list[str]] = Depends(get_errors_from_session),
):
    try:
        # Retrieves a product from the database by its ID.
        product = get_product_by_id(product_id, db)

        # Retrieves all SKUs associated with a given product ID.
        skus = get_skus_by_id(product_id, db)

        if product is None or skus is None:
            # For traceback
            logger.exception(f"Product not found: {product_id}")
            return RedirectResponse(url="/products", status_code=303)
    except Exception as e:
        # For traceback
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return templates.TemplateResponse(
        "product_detail.html",
        {"request": request, "product": product, "skus": skus, "user": user, "errors": errors},
    )


@router.post("/add")
def add_to_cart(
    request: Request,
    form: AddToCartForm = Depends(AddToCartForm.as_form),
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    try:
        # Validate if the SKU exists and the quantity is acceptable for adding to the cart.
        errors = validate_add_to_cart(
            sku_id=form.sku_id,
            quantity=form.quantity,
            product_id=form.product_id,
            db=db,
        )

        # If a validation error occurs, return it to the frontend for display.
        if errors:
            request.session["errors"] = errors
            return RedirectResponse(url=f"/products/{form.product_id}", status_code=303)

        # Add a SKU to the user's cart, or increment the quantity if it already exists.
        process_add_to_cart(
            sku_id=form.sku_id,
            quantity=form.quantity,
            user=user,
            session_token=session_token,
            db=db,
        )
    except RedirectHomeException as e:
        raise RedirectHomeException("Invalid SKU or other cart error") from e
    except Exception as e:
        # For traceback
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return RedirectResponse(url="/cart", status_code=303)