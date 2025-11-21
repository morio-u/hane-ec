from typing import Optional, Union
from starlette.templating import _TemplateResponse
from sqlalchemy.orm import Session
from pydantic import ValidationError
from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from app.core.exception import RedirectHomeException
from app.crud.admin.products import save_product_images, save_product_with_form
from app.crud.common.masters import (
    get_all_brands,
    get_all_colors,
    get_all_sizes,
    get_all_category_tree,
)
from app.crud.admin.sku import save_skus_with_form
from app.crud.shop.products import (
    get_all_products,
    get_products_with_quantity,
    get_product_with_category_tree,
    get_skus_by_id,
)
from app.dependencies.auth import get_current_admin_user
from app.dependencies.session import get_errors_from_session
from app.models.admin_user import AdminUser
from app.models.product import ProductStatusEnum, PurchaseTypeEnum
from app.models.sku import SkuStatusEnum
from app.schemas.admin.products import SaveProductForm
from app.utils.constants import (
    cast_dict_fields_to_int,
    get_skus_with_form,
    is_dict_empty,
)
from app.validators.admin.products import (
    format_validation_errors,
    render_form_with_errors,
    validate_save_product_form,
)
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
        logger.exception(f"Unexpected error in get_products: {e}")
        raise RedirectHomeException("Unexpected error")

    return templates.TemplateResponse(
        "products.html",
        {"request": request, "products": products_with_qty, "user": user},
    )


@router.get("/create", response_class=HTMLResponse, name="create_product")
def create_product(
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[AdminUser] = Depends(get_current_admin_user),
) -> _TemplateResponse:
    try:
        product = None
        skus = None
        brands = get_all_brands(db)
        colors = get_all_colors(db)
        sizes = get_all_sizes(db)
        departments, categories, subcategories = get_all_category_tree(db)

    except Exception as e:
        # For traceback
        logger.exception(f"Unexpected error in create_product: {e}")
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
        },
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
        product = get_product_with_category_tree(product_id, db)

        # Retrieves all SKUs associated with a given product ID.
        skus = get_skus_by_id(product_id, db)

        # Retrieves master data from the database
        brands = get_all_brands(db)
        colors = get_all_colors(db)
        sizes = get_all_sizes(db)
        departments, categories, subcategories = get_all_category_tree(db)

        if product is None:
            # For traceback
            logger.exception(f"Product not found: {product_id}")
            return RedirectResponse(url="/admin/products", status_code=303)
    except Exception as e:
        # For traceback
        logger.exception(f"Unexpected error in get_product_detail: {e}")
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
    image_files: list[UploadFile] = File(default_factory=list),
    db: Session = Depends(get_db),
    user: Optional[AdminUser] = Depends(get_current_admin_user),
) -> RedirectResponse:
    try:
        # TODO:For pydantic exception handler.
        # The routing function must be asynchronous.
        form_all_data = await request.form()

        # Converts a string to a number.
        int_fields = [
            "id",
            "brand_id",
            "purchase_type",
            "department_id",
            "category_id",
            "subcategory_id",
        ]
        form_dict = cast_dict_fields_to_int(dict(form_all_data), int_fields)

        # Save the raw data.
        request._form_data = form_dict

        # Retrieves skus from form.
        skus_from_form = get_skus_with_form(form_all_data)

        # Pydantic Validation
        try:
            form_data = SaveProductForm(**form_dict)
        except ValidationError as exc:
            # Converts a Pydantic ValidationError object into a list of user-friendly strings.
            errors = format_validation_errors(exc)
            return render_form_with_errors(
                request, errors, form_dict, skus_from_form, db
            )

        # Custom Validation
        errors = validate_save_product_form(form_data)

        # If a validation error occurs, return it to the frontend for display.
        if errors:
            return render_form_with_errors(
                request, errors, form_dict, skus_from_form, db
            )

        # create or update Product
        saved_product = save_product_with_form(form_data, db)

        if saved_product is None:
            # For traceback
            logger.warning(f"Product not found: {form_data.id}")
            return RedirectResponse(url="/admin/products", status_code=303)
        # TODO:Add RedirectDashboardException

        # If skus are entered, save them.
        if not is_dict_empty(skus_from_form):
            _ = save_skus_with_form(skus_from_form, saved_product.id, db)

        if form_data:
            # If images are entered, save them.
            await save_product_images(form_data, image_files, db)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
    except Exception as e:
        # For traceback
        logger.exception(f"Unexpected error in save_product: {e}")
        raise RedirectHomeException("Unexpected error")

    return RedirectResponse(
        url=f"/admin/products/{ saved_product.id }", status_code=303
    )
