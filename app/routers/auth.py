from datetime import timedelta
from typing import Dict
from fastapi import APIRouter, Request, HTTPException, status, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.jwt import create_access_token
from app.core.config import settings
from app.crud.user import get_user_by_email, create_user, authenticate_user
from app.database import get_db
from app.schemas.auth import OAuth2PasswordRequestLoginForm
from app.schemas.user import UserCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("/login", response_class=HTMLResponse)
def read_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", name="login")
def login(
    db: Session = Depends(get_db),
    # TODO: Move to OAuth2PasswordRequestLoginForm
    email: str = Form(...),
    password: str = Form(...),
) -> Dict[str, str]:
    """
    Login Processing
    Receives form_data.email / form_data.password,
    and returns a JWT upon successful authentication.
    """
    user_from_db = authenticate_user(db, email, password)
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_from_db.email}, expires_delta=access_token_expires
    )

    redirect = RedirectResponse(url="/", status_code=303)
    redirect.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60,
        samesite="lax",
    )
    return redirect


@router.get("/logout")
def logout():
    redirect = RedirectResponse(url="/", status_code=303)
    redirect.delete_cookie(key="access_token")
    return redirect


@router.get("/signup", response_class=HTMLResponse)
def read_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
def signup(
    db: Session = Depends(get_db),
    # TODO: Move to UserCreate
    last_name: str = Form(...),
    first_name: str = Form(...),
    gender: int = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    is_send_newsletter: bool = Form(False),
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check already registered users
    user_from_db = get_user_by_email(db, email)
    if user_from_db:
        raise HTTPException(status_code=400, detail="Email already exists")

    # New User Registration
    new_user = create_user(
        db,
        last_name,
        first_name,
        gender,
        phone_number,
        email,
        password,
        is_send_newsletter,
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.email)}, expires_delta=access_token_expires
    )

    redirect = RedirectResponse(url="/", status_code=303)
    redirect.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60,
        samesite="lax",
    )
    return redirect
