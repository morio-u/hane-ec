from typing import List
from sqlalchemy.orm import Session
from app.models import Brand, Category, Color, Department, Size, Subcategory


def get_all_brands(db: Session) -> List[Brand]:
    return db.query(Brand).all()


def get_all_colors(db: Session) -> List[Color]:
    return db.query(Color).all()


def get_all_sizes(db: Session) -> List[Size]:
    return db.query(Size).all()


def get_category_tree(db: Session):
    departments = get_all_departments(db)
    categories = get_all_categories(db)
    subcategories = get_all_subcategories(db)

    return departments, categories, subcategories


def get_all_departments(db: Session):
    return db.query(Department).all()


def get_all_categories(db):
    return db.query(Category).all()


def get_all_subcategories(db):
    return db.query(Subcategory).all()