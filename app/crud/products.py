from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Product, Sku


def get_all_products(db: Session) -> List[Product]:
    """
    Retrieves all products from the database.

    Parameters:
        db (Session): The active SQLAlchemy database session.

    Returns:
        List[Product]: A list of all Product records (empty list if none found).
    """
    return db.query(Product).all()


def get_product_by_id(product_id: int, db: Session) -> Optional[Product]:
    """
    Retrieves a product from the database by its ID.

    Parameters:
        product_id (int): The unique identifier of the product to retrieve.
        db (Session): The SQLAlchemy database session.

    Returns:
        Optional[Product]: The product with the given ID, or None if not found.
    """
    return db.query(Product).filter(Product.id == product_id).first()


def get_skus_by_id(product_id: int, db: Session) -> List[Sku]:
    """
    Retrieves all SKUs associated with a given product ID.

    Parameters:
        product_id (int): The ID of the product.
        db (Session): The SQLAlchemy database session.

    Returns:
        List[Sku]: A list of SKUs for the given product (empty if not found).
    """
    product = get_product_by_id(product_id, db)
    if product is None:
        return []

    return product.skus
