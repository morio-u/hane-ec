from datetime import timedelta
from starlette.templating import _TemplateResponse
from fastapi import APIRouter, HTTPException, Request, status, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.jwt import create_admin_access_token
from app.core.config import settings
from app.crud.admin.user import (
    authenticate_admin_user,
)
from app.core.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/admin")


@router.get("/login", response_class=HTMLResponse)
def read_login_form(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", name="login")
def login(
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...),
) -> RedirectResponse:
    """
    Login Processing
    Receives form_data.email / form_data.password,
    and returns a JWT upon successful authentication.
    """
    user_from_db = authenticate_admin_user(db, email, password)
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_admin_access_token(
        data={"sub": user_from_db.email}, expires_delta=access_token_expires
    )

    redirect = RedirectResponse(url="/admin", status_code=303)
    redirect.set_cookie(
        key="admin_access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60,
        samesite="lax",
    )
    return redirect


@router.get("/logout")
def logout() -> RedirectResponse:
    redirect = RedirectResponse(url="/admin/auth/login", status_code=303)
    redirect.delete_cookie(key="admin_access_token")
    return redirect
