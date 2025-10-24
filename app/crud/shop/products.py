from typing import List, Dict, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
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


def get_skus_by_products(products: List[Product], db: Session) -> Dict[int, List[Sku]]:
    """
    Retrieves SKUs for multiple products based on their IDs.

    Parameters:
        product_ids (List[Product]): A list of product IDs.
        db (Session): The SQLAlchemy database session.

    Returns:
        Dict[int, List[Sku]]: A dictionary mapping product_id -> list of SKUs.
                              Empty list for products that have no SKUs.
    """

    if not products:
        return {}

    product_ids = [p.id for p in products]
    products = (
        db.query(Product)
        .options(joinedload(Product.skus))
        .filter(Product.id.in_(product_ids))
        .all()
    )

    # 2. 結果を {product_id: [skus]} の形に整形
    product_sku_map = {product.id: product.skus for product in products}

    # 3. 存在しなかったIDも空リストで埋める（オプション）
    for pid in product_ids:
        product_sku_map.setdefault(pid, [])

    return product_sku_map


def get_products_with_quantity(product_ids: int, db: Session) -> List[Product]:
    """
    Retrieves a list of products along with the total stock quantity for each.

    This function aggregates the stock quantities from the `Sku` table,
    summing them by `product_id` for the specified products only. It then
    performs an OUTER JOIN with the `Product` table to include all given
    products, even those with no SKUs (stock count will be 0 in that case).

    Parameters:
        db (Session): The SQLAlchemy database session.
        product_ids (List[int]): A list of product IDs to retrieve.

    Returns:
        List[Product]: A list of Product objects. Each product instance includes
                    an additional dynamic attribute `total_stock` representing
                    the sum of all related SKUs' stock quantities.
    """

    # Subquery: Aggregate SKU inventory by product_id
    stock_subquery = (
        db.query(
            Sku.product_id.label("product_id"),
            func.coalesce(func.sum(Sku.stock_quantity), 0).label("total_quantity"),
        )
        .filter(Sku.product_id.in_(product_ids))
        .group_by(Sku.product_id)
        .subquery()
    )

    # LEFT JOIN on the total_quantity column in the Product
    products = (
        db.query(Product, stock_subquery.c.total_quantity)
        .outerjoin(stock_subquery, Product.id == stock_subquery.c.product_id)
        .filter(Product.id.in_(product_ids))
        .all()
    )

    # Return formatted for easy handling in dictionary format, etc. (optional)
    result = []
    for product, total_stock in products:
        product.total_quantity = total_stock or 0
        result.append(product)

    return result
