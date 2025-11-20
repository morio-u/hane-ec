from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sku import Sku


def get_skus_by_id(product_id: int, db: Session) -> Optional[List[Sku]]:
    return db.query(Sku).filter(Sku.product_id == product_id).all()
