from datetime import timedelta
from typing import Dict
from fastapi import APIRouter, Request, HTTPException, status, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.schemas.auth import OAuth2PasswordRequestLoginForm
from app.core.jwt import create_access_token
from app.core.config import settings
from app.crud.user import authenticate_user
from app.database import get_db

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
        data={"sub": user_from_db.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": settings.TOKEN_TYPE}