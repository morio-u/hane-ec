from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.product import Product

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")

@router.get("/products", response_class=HTMLResponse)
def get_products(request: Request, db: Session = Depends(get_db), user = Depends(get_current_user)):
    products = db.query(Product).all()
    return templates.TemplateResponse(
        "products.html", {"request": request, "products": products, "user": user}
    )

@router.get("/products/{product_id}", response_class=HTMLResponse)
def get_product_detail(request: Request, product_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        skus = product.skus
    else:
        return RedirectResponse(url="/products", status_code=302)

    return templates.TemplateResponse(
        "product_detail.html", {"request": request, "product": product, "skus": skus, "user": user}
    )
    