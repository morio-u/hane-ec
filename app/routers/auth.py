from datetime import timedelta
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.schemas import OAuth2PasswordRequestLoginForm
from app.core.jwt import create_access_token
from app.core.config import settings
from app.crud.user import authenticate_user
from app.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestLoginForm = Depends()) -> Dict[str, str]:
    """
    Login Processing
    Receives form_data.email / form_data.password,
    and returns a JWT upon successful authentication.
    """
    user_from_db = authenticate_user(db, form_data.email, form_data.password)
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