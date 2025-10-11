from typing import Optional
from starlette.templating import _TemplateResponse
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/admin")


@router.get("/", response_class=HTMLResponse, name="dashboard")
def dashboard(
    request: Request, user: Optional[User] = Depends(get_current_user)
) -> _TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@router.get("/ui-carousel.html", response_class=HTMLResponse)
async def ui_carousel(request: Request):
    return templates.TemplateResponse("ui-carousel.html", {"request": request})