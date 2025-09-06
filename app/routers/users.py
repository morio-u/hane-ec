from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.routers.auth import oauth2_scheme
from app.crud.user import get_user_by_email, create_user
from app.database import get_db

router = APIRouter()

class UserCreate(BaseModel):
    last_name: str
    middle_name: Optional[str] = None
    first_name: str
    gender: int
    phone_number: str
    email: str
    password: str
    is_send_newsletter: bool

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(username, db)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/signup")
def signup(form_data: UserCreate, db: Session = Depends(get_db)):
    # Check already registered users
    user_from_db = get_user_by_email(db, form_data.email)
    if user_from_db:
        raise HTTPException(status_code=400, detail="Email already exists")

    # New User Registration
    new_user = create_user(
        db,
        form_data.last_name,
        form_data.first_name,
        form_data.gender,
        form_data.phone_number,
        form_data.email,
        form_data.password,
        form_data.is_send_newsletter,
        form_data.middle_name,
    )
    return {"username": new_user.last_name}

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "disabled": current_user["disabled"]}