from typing import List
from sqlalchemy.orm import Session
from app.crud.products import get_product_by_id
from app.crud.sku import get_sku_by_id


def validate_add_to_cart(sku_id: int, quantity: int, product_id: int, db: Session) -> List[str]:
    """
    Validate if the SKU exists and the quantity is acceptable for adding to the cart.

    Args:
        sku_id (int): The ID of the SKU to validate.
        quantity (int): The requested quantity to add.
        db (Session): The database session for querying SKU information.

    Returns:
        List[str]: A list of error messages. Empty if no errors.
    """
    errors = []

    product = get_product_by_id(product_id, db)
    sku = get_sku_by_id(sku_id, db)

    if product is None or sku is None:
        errors.append("Product not found.")

    if not (1 <= quantity <= 2):
        errors.append("Quantity must be between 1 and 2.")

    if quantity > sku.stock_quantity:
        errors.append("The requested quantity exceeds available stock.")

    return errors
