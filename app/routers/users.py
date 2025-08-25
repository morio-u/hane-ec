from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.routers.auth import oauth2_scheme
from app.crud.user import get_user_by_username

router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
