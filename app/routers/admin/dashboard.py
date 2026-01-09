from typing import Optional
from starlette.templating import _TemplateResponse
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies.auth import get_current_admin_user
from app.models.admin_user import AdminUser

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/admin")


@router.get("", response_class=HTMLResponse, name="dashboard")
def dashboard(
    request: Request, user: Optional[AdminUser] = Depends(get_current_admin_user)
) -> _TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
