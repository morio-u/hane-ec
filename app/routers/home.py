from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from app.dependencies.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")

@router.get("/")
def home(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": current_user}
    )