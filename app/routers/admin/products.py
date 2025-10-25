from typing import Optional, Union
from starlette.templating import _TemplateResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from app.core.exception import RedirectHomeException
from app.crud.common.masters import (
    get_all_brands,
    get_all_colors,
    get_all_sizes,
    get_all_category_tree,
)
from app.crud.shop.products import (
    get_all_products,
    get_product_by_id,
    get_products_with_quantity,
    get_skus_by_id,
)
from app.dependencies.auth import get_current_admin_user
from app.dependencies.session import get_errors_from_session
from app.models.admin_user import AdminUser
from app.models.product import Product, ProductStatusEnum, PurchaseTypeEnum
from app.models.sku import SkuStatusEnum
from app.schemas.admin.products import SaveProductForm
from app.utils.constants import get_skus_from_form
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
        "products.html",
        {"request": request, "products": products_with_qty, "user": user},
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

        brands = get_all_brands(db)
        colors = get_all_colors(db)
        sizes = get_all_sizes(db)
        departments, categories, subcategories = get_all_category_tree(db)

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
            "brands": brands,
            "departments": departments,
            "categories": categories,
            "subcategories": subcategories,
            "colors": colors,
            "sizes": sizes,
            "ProductStatusEnum": ProductStatusEnum,
            "PurchaseTypeEnum": PurchaseTypeEnum,
            "SkuStatusEnum": SkuStatusEnum,
            "errors": errors,
        },
    )


@router.post("/save")
async def save_product(
    request: Request,
    form: SaveProductForm = Depends(SaveProductForm.as_form),
    db: Session = Depends(get_db),
    user: Optional[AdminUser] = Depends(get_current_admin_user),
) -> RedirectResponse:
    # The routing function must be asynchronous.
    form_data = await request.form()

    skus = get_skus_from_form(form_data)

    product = db.query(Product).filter(Product.id == form.id).first()

    if product is None or not skus:
        # For traceback
        logger.exception(f"Product not found: {form.id}")
        return RedirectResponse(url="/admin/products", status_code=303)
    # TODO:Add RedirectDashboardException

    product.internal_part_number = form.internal_part_number
    product.manufacturer_part_number = form.manufacturer_part_number
    product.name = form.name
    product.brand_id = form.brand_id
    product.subcategory_id = form.subcategory_id
    product.purchase_type = form.purchase_type
    product.price_excluding_tax = form.price_excluding_tax
    product.cost_price = form.cost_price
    product.status = form.status
    product.description = form.description

    try:
        db.add(product)
        db.commit()
        db.refresh(product)
    except Exception as e:
        db.rollback()
        raise e

    return RedirectResponse(url=f"/admin/products/{ form.id }", status_code=303)
