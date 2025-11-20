from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sku import Sku
from app.crud.common.sku import get_skus_by_id
from app.schemas.admin.products import SaveProductForm


def create_skus_with_form(
    new_product_id: int, form_data: SaveProductForm, db: Session
) -> Optional[List[Sku]]:
    new_skus = []
    for sku_id, fields in form_data.items():
        new_sku = Sku(
            product_id=new_product_id,
            barcode=fields.barcode,
            color_id=fields.color_id,
            size_id=fields.size_id,
            stock_quantity=fields.stock_quantity,
            special_price=fields.special_price,
            status=fields.status,
        )
        db.add(new_sku)
        new_skus.append(new_sku)

    if not new_skus:
        return None
    return new_skus


def update_skus_with_form(skus: dict, db: Session) -> Optional[List[Sku]]:
    """
    Updates multiple SKU records in the database.

    Iterates over the given dictionary, finds each SKU by ID,
    and updates its fields using `setattr()`.
    Changes are applied to the current session but not committed here.

    Args:
        db (Session): SQLAlchemy database session.
        skus (dict): Dictionary in the format {sku_id: {"field": value, ...}, ...}.

    Returns:
        Optional[List[Sku]]: List of updated SKU objects.
        Returns None if no SKUs were updated.

    Notes:
        - SKUs not found in the database are skipped.
        - Commit should be handled by the caller.
    """
    updated_skus = []
    for sku_id, fields in skus.items():
        sku = db.query(Sku).filter(Sku.id == sku_id).first()
        if not sku:
            continue
        for key, value in fields.items():
            # For nullable column
            if value == "":
                value = None
            setattr(sku, key, value)
        updated_skus.append(sku)

    if not updated_skus:
        return None
    return updated_skus


def save_skus_with_form(
    form_skus: dict, product_id: int, db: Session
) -> Optional[List[Sku]]:
    """
    Synchronizes SKU data between form and database.

    - Updates existing SKUs
    - Creates new SKUs
    - Optionally deletes missing SKUs
    """
    db_skus = get_skus_by_id(product_id, db)
    db_sku_map = {sku.id: sku for sku in db_skus}

    # 1️⃣ UPDATE or CREATE
    for sku_id, fields in form_skus.items():
        if sku_id in db_sku_map:
            # --- update existing ---
            sku = db_sku_map[sku_id]
            sku.barcode = fields["barcode"]
            sku.color_id = fields["color_id"]
            sku.size_id = fields["size_id"]
            sku.stock_quantity = fields["stock_quantity"]
            sku.special_price = fields["special_price"]
            sku.status = fields["status"]
        else:
            # --- create new ---
            new_sku = Sku(
                product_id=product_id,
                barcode=fields["barcode"],
                color_id=fields["color_id"],
                size_id=fields["size_id"],
                stock_quantity=fields["stock_quantity"],
                special_price=fields["special_price"],
                status=fields["status"],
            )
            db.add(new_sku)

    # 2️⃣ DELETE (optional)
    form_ids = set(form_skus.keys())
    db_ids = set(db_sku_map.keys())
    for remove_id in db_ids - form_ids:
        db.delete(db_sku_map[remove_id])

    db.flush()
    return get_skus_by_id(product_id, db)
