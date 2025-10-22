from typing import Optional, Union
from starlette.templating import _TemplateResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from app.core.exception import RedirectHomeException
from app.crud.shop.products import get_all_products, get_product_by_id, get_products_with_quantity, get_skus_by_id
from app.dependencies.auth import get_current_admin_user
from app.dependencies.session import get_errors_from_session
from app.models.admin.admin_user import AdminUser
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/admin")


@router.get("", response_class=HTMLResponse, name="products")
def get_products(
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[AdminUser] = Depends(get_current_admin_user),
) -> _TemplateResponse:
    try:
        # Retrieves all products from the database.
        products = get_all_products(db)

        product_ids = [p.id for p in products]
        products_with_qty = get_products_with_quantity(product_ids, db)

    except Exception as e:
        # For traceback
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return templates.TemplateResponse(
        "products.html", {"request": request, "products": products_with_qty, "user": user}
    )


@router.get("/{product_id}", response_class=HTMLResponse, response_model=None)
def get_product_detail(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
    user: Optional[AdminUser] = Depends(get_current_admin_user),
    errors: Optional[list[str]] = Depends(get_errors_from_session),
) -> Union[_TemplateResponse, RedirectResponse]:
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
        {
            "request": request,
            "product": product,
            "skus": skus,
            "user": user,
            "errors": errors,
        },
    )