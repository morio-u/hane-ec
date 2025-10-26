from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sku import Sku

def update_skus_from_form(skus: dict, db: Session) -> Optional[List[Sku]]:
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