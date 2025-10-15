from typing import Optional
from sqlalchemy.orm import Session
from app.models.shop.sku import Sku


def get_sku_by_id(sku_id: int, db: Session) -> Optional[int]:
    """
    Retrieve a single SKU object by its unique ID.

    Args:
        sku_id (int): The unique identifier of the SKU.
        db (Session): SQLAlchemy database session.

    Returns:
        Sku | None: The SKU object if found, otherwise None.
    """
    return db.query(Sku).filter(Sku.id == sku_id).first()
