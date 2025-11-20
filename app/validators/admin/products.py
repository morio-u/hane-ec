from decimal import Decimal
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import List
from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.crud.common.masters import (
    get_all_brands,
    get_all_colors,
    get_all_sizes,
    get_all_category_tree,
)
from app.models.product import ProductStatusEnum, PurchaseTypeEnum
from app.models.sku import SkuStatusEnum

templates = Jinja2Templates(directory="app/templates/admin")


def validate_save_product_form(form: dict) -> List[str]:

    errors = []

    # Check required items
    required_fields = {
        "INTERNAL PART NUMBER": form.internal_part_number,
        "SUBCATEGORY": form.subcategory_id,
        "BRAND": form.brand_id,
        "PRODUCT NAME": form.name,
        "PURCHASE TYPE": form.purchase_type,
        "STATUS": form.status,
    }

    for field_name, value in required_fields.items():
        if value is None or str(value).strip() == "":
            errors.append(f"{field_name} is required.")

    # If there is an error in the required field check, return it.
    if errors:
        return errors

    if not isinstance(form.internal_part_number, str):
        errors.append("INTERNAL PART NUMBER must be a string.")
    if form.manufacturer_part_number and not isinstance(
        form.manufacturer_part_number, str
    ):
        errors.append("MANUFACTURER PART NUMBER must be a string.")
    if not isinstance(form.name, str):
        errors.append("PRODUCT NAME must be a string.")
    if form.subcategory_id and not isinstance(form.subcategory_id, int):
        errors.append("SUBCATEGORY must be a integer.")
    if not isinstance(form.brand_id, int):
        errors.append("BRAND is invalid.")
    if form.shipping_rule_id and not isinstance(form.shipping_rule_id, int):
        errors.append("SHIPPING RULE is invalid.")
    if not isinstance(form.description, str):
        errors.append("DESCRIPTION must be a string.")
    if not isinstance(form.purchase_type, int):
        errors.append("PURCHASE TYPE is invalid.")
    if not isinstance(form.price_excluding_tax, (Decimal)):
        errors.append("PRICE (EXCL. TAX) must be a decimal.")
    if not isinstance(form.cost_price, (Decimal)):
        errors.append("COST PRICE must be a decimal.")
    if not isinstance(form.status, str):
        errors.append("STATUS is invalid.")

    return errors


def format_validation_errors(exc: ValidationError) -> List[str]:
    errors = []
    for error in exc.errors():
        field = error["loc"][0]
        msg = error["msg"]

        field_label_map = {
            "internal_part_number": "INTERNAL PART NUMBER",
            "manufacturer_part_number": "MANUFACTURER PART NUMBER",
            "name": "PRODUCT NAME",
            "brand_id": "BRAND",
            "shipping_rule_id": "SHIPPING RULE",
            "department_id": "DEPARTMENT",
            "category_id": "CATEGORY",
            "subcategory_id": "SUBCATEGORY",
            "purchase_type": "PURCHASE TYPE",
            "price_excluding_tax": "PRICE (EXCL. TAX)",
            "cost_price": "COST PRICE",
            "status": "STATUS",
            "description": "DESCRIPTION",
            "image_files": "PRODUCT IMAGES",
        }
        field_label = field_label_map.get(field, field)
        errors.append(f"{field_label} is invalid. {msg}.")

    return errors


def render_form_with_errors(
    request: Request, errors: List, form_dict: dict, skus_from_form: dict, db: Session
):
    id_value = form_dict.get("id", "")
    if id_value:
        # If a validation error occurs, return it to the frontend for display.
        request.session["errors"] = errors

        # If 'id' exists (Update/Save): Redirect to product detail page.
        return RedirectResponse(url=f"/admin/products/{ id_value }", status_code=303)

    # Retrieves master data from the database.
    departments, categories, subcategories = get_all_category_tree(db)

    # If 'id' is missing or empty (Create): Redirect to the creation page.
    return templates.TemplateResponse(
        "product_detail.html",
        {
            "request": request,
            "errors": errors,
            "product": form_dict,
            "skus": list(skus_from_form.values()),
            "brands": get_all_brands(db),
            "departments": departments,
            "categories": categories,
            "subcategories": subcategories,
            "colors": get_all_colors(db),
            "sizes": get_all_sizes(db),
            "ProductStatusEnum": ProductStatusEnum,
            "PurchaseTypeEnum": PurchaseTypeEnum,
            "SkuStatusEnum": SkuStatusEnum,
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
