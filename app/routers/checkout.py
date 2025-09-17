import json
from fastapi import Request, Response, APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dependencies.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")

@router.get("")
def view_checkout_form(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "checkout_form.html",
        {"request": request, "user": user}
    )

@router.post("/confirm", name="create_order")
def create_order(request: Request, user=Depends(get_current_user)):
    return {"message": "Order created"}