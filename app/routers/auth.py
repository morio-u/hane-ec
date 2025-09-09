from datetime import timedelta
from typing import Dict
from fastapi import APIRouter, Request, HTTPException, status, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.jwt import create_access_token
from app.core.config import settings
from app.crud.user import authenticate_user
from app.database import get_db
from app.schemas.auth import OAuth2PasswordRequestLoginForm

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")

@router.get("/login", response_class=HTMLResponse)
def read_login_form(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request}
    )

@router.post("/login", name="login")
def login(
        db: Session = Depends(get_db),
        # TODO: Move to OAuth2PasswordRequestLoginForm
        email: str = Form(...),
        password: str = Form(...)
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
        samesite="lax"
    )
    return redirect

@router.get("/logout")
def logout():
    redirect = RedirectResponse(url="/", status_code=303)
    redirect.delete_cookie(key="access_token")
    return redirect