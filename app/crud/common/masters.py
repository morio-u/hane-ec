from typing import List
from sqlalchemy.orm import Session
from app.models import Brand, Category, Color, Department, Size, Subcategory


def get_all_brands(db: Session) -> List[Brand]:
    return db.query(Brand).order_by(Brand.id).all()


def get_all_colors(db: Session) -> List[Color]:
    return db.query(Color).order_by(Color.id).all()


def get_all_sizes(db: Session) -> List[Size]:
    return db.query(Size).order_by(Size.id).all()


def get_all_category_tree(db: Session):
    departments = get_all_departments(db)
    categories = get_all_categories(db)
    subcategories = get_all_subcategories(db)

    return departments, categories, subcategories


def get_all_departments(db: Session):
    return db.query(Department).order_by(Department.id).all()


def get_all_categories(db):
    return db.query(Category).order_by(Category.id).all()


def get_all_subcategories(db):
    return db.query(Subcategory).order_by(Subcategory.id).all()
