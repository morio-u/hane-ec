from typing import Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.admin.products import SaveProductForm


def update_product_with_form(
    form_data: SaveProductForm, db: Session
) -> Optional[Product]:
    product = db.query(Product).filter(Product.id == form_data.id).first()

    if not product:
        return None

    if product is not None:
        product.internal_part_number = form_data.internal_part_number
        product.manufacturer_part_number = form_data.manufacturer_part_number
        product.name = form_data.name
        product.brand_id = form_data.brand_id
        product.subcategory_id = form_data.subcategory_id
        product.purchase_type = form_data.purchase_type
        product.price_excluding_tax = form_data.price_excluding_tax
        product.cost_price = form_data.cost_price
        product.status = form_data.status
        product.description = form_data.description

    return product


def create_product_with_form(form_data: SaveProductForm, db: Session) -> Product:
    product = Product(
        internal_part_number=form_data.internal_part_number,
        manufacturer_part_number=form_data.manufacturer_part_number,
        name=form_data.name,
        brand_id=form_data.brand_id,
        subcategory_id=form_data.subcategory_id,
        purchase_type=form_data.purchase_type,
        price_excluding_tax=form_data.price_excluding_tax,
        cost_price=form_data.cost_price,
        status=form_data.status,
        description=form_data.description,
    )
    db.add(product)
    db.flush()
    return product


def save_product_with_form(
    form_data: SaveProductForm, db: Session
) -> Optional[Product]:
    if form_data.id is None:
        saved_product = create_product_with_form(form_data, db)
    else:
        saved_product = update_product_with_form(form_data, db)

    if not saved_product:
        return None
    return saved_product
