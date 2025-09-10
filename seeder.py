from app.database import SessionLocal
from app.models.department import Department
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models.brand import Brand
from app.models.product import Product, PurchaseTypeEnum, ProductStatusEnum

def seed_departments(db):
    departments = [
        Department(id=1, name="Electronics"),
    ]
    db.add_all(departments)
    db.commit()

def seed_categories(db):
    categories = [
        Category(id=1, department_id=1, name="Wearables"),
    ]
    db.add_all(categories)
    db.commit()

def seed_subcategories(db):
    subcategories = [
        Subcategory(id=1, category_id=1, name="Earbuds"),
        Subcategory(id=2, category_id=1, name="Smartwatches"),
    ]
    db.add_all(subcategories)
    db.commit()


def seed_brands(db):
    brands = [
        Brand(id=1, name="SoundCo"),
        Brand(id=2, name="TechTime"),
    ]
    db.add_all(brands)
    db.commit()

def seed_products(db):
    products = [
        Product(
            internal_part_number="P000000000001",
            manufacturer_part_number="M-001",
            subcategory_id=1,
            brand_id=1,
            name="Wireless Bluetooth Earbuds",
            description="High quality earbuds with noise cancellation.",
            purchase_type=PurchaseTypeEnum.purchase.value,
            price_excluding_tax=59.99,
            cost_price=25.00,
            status=ProductStatusEnum.active,
        ),
        Product(
            internal_part_number="P000000000002",
            manufacturer_part_number="M-002",
            subcategory_id=2,
            brand_id=2,
            name="Smartwatch Pro 3",
            description="Smartwatch with health tracking and GPS.",
            purchase_type=PurchaseTypeEnum.purchase.value,
            price_excluding_tax=199.99,
            cost_price=120.00,
            status=ProductStatusEnum.active,
        ),
    ]

    db.add_all(products)
    db.commit()

def seed_all():
    db = SessionLocal()
    try:
        seed_departments(db)
        seed_categories(db)
        seed_subcategories(db)
        seed_brands(db)
        seed_products(db)
    finally:
        db.close()

if __name__ == "__main__":
    seed_all()