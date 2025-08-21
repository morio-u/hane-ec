from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from database import get_db
from models import Product

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/products", response_class=HTMLResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse(
        "products.html", {"request": request, "products": products}
    )
