from typing import List
from sqlalchemy.orm import Session
from app.models.shop import Brand, Color, Size


def get_all_brands(db: Session) -> List[Brand]:
    return db.query(Brand).all()

def get_all_colors(db: Session) -> List[Color]:
    return db.query(Color).all()

def get_all_sizes(db: Session) -> List[Size]:
    return db.query(Size).all()