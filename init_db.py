from app.database import SessionLocal, engine
from app.models.product import Base, Product

Base.metadata.create_all(bind=engine)  # テーブル作成

db = SessionLocal()
db.add_all([
    Product(name="商品A", price=1000),
    Product(name="商品B", price=2000),
])
db.commit()
db.close()