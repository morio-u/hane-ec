from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, user: Optional[User] = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
