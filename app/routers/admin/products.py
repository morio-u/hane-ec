from typing import Optional
from starlette.templating import _TemplateResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from app.core.exception import RedirectHomeException
from app.crud.shop.products import get_all_products, get_products_with_quantity
from app.dependencies.auth import get_current_admin_user
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
