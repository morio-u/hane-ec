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
    create_admin_user,
    get_admin_user_by_email,
)
from app.core.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/admin")


@router.get("/login", response_class=HTMLResponse)
def read_login_form(request: Request):
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
    redirect = RedirectResponse(url="/", status_code=303)
    redirect.delete_cookie(key="admin_access_token")
    return redirect


@router.get("/signup", response_class=HTMLResponse)
def read_signup_form(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
def signup(
    db: Session = Depends(get_db),
    last_name: str = Form(...),
    first_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    role_id: str = Form(...),
) -> RedirectResponse:
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check already registered users
    user_from_db = get_admin_user_by_email(db, email)
    if user_from_db:
        raise HTTPException(status_code=400, detail="Email already exists")

    # New User Registration
    new_user = create_admin_user(
        db,
        last_name,
        first_name,
        email,
        password,
        role_id,
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_admin_access_token(
        data={"sub": str(new_user.email)}, expires_delta=access_token_expires
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
