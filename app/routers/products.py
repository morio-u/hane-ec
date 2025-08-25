from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.database import get_db
from app.models import Product

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")

@router.get("/products", response_class=HTMLResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse(
        "products.html", {"request": request, "products": products}
    )

@router.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )