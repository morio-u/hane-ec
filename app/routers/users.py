from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email, create_user
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.user import UserCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")

@router.get("/signup", response_class=HTMLResponse)
def read_signup_form(request: Request):
    return templates.TemplateResponse(
        "signup.html", {"request": request}
    )

@router.post("/signup")
def signup(
        db: Session = Depends(get_db),
        # TODO: Move to UserCreate
        last_name: str = Form(...),
        first_name: str = Form(...),
        middle_name: str = Form(None),
        gender: int = Form(...),
        phone_number: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
        is_send_newsletter: bool = Form(False)
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
        middle_name,
    )
    return {"username": new_user.last_name}

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "disabled": current_user["disabled"]}