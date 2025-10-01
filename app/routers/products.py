from fastapi import Request, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.crud.products import get_all_products, get_product_by_id, get_skus_by_id
from app.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("/products", response_class=HTMLResponse)
def get_products(
    request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    # Retrieves all products from the database.
    products = get_all_products(db)

    return templates.TemplateResponse(
        "products.html", {"request": request, "products": products, "user": user}
    )


@router.get("/products/{product_id}", response_class=HTMLResponse)
def get_product_detail(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # Retrieves a product from the database by its ID.
    product = get_product_by_id(product_id, db)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Retrieves all SKUs associated with a given product ID.
    skus = get_skus_by_id(product_id, db)
    if skus is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return templates.TemplateResponse(
        "product_detail.html",
        {"request": request, "product": product, "skus": skus, "user": user},
    )
