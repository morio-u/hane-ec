from jose import jwt, JWTError
from typing import Optional
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.crud.shop.user import get_user_by_email
from app.crud.admin.user import get_admin_user_by_email
from app.models.user import User
from app.models.admin_user import AdminUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """
    Retrieve the currently authenticated user based on the access token stored in cookies.

    Args:
        request (Request): FastAPI request object, used to access cookies.
        db (Session): Database session dependency, used to query the user.

    Returns:
        Optional[User]: The authenticated User object if the token is valid and the user exists;
                        otherwise, returns None if no token is present.

    Raises:
        HTTPException: If the token is invalid or the user does not exist in the database.
    """
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_admin_user(
    request: Request, db: Session = Depends(get_db)
) -> Optional[AdminUser]:
    """
    Retrieve the currently authenticated user based on the access token stored in cookies.

    Args:
        request (Request): FastAPI request object, used to access cookies.
        db (Session): Database session dependency, used to query the user.

    Returns:
        Optional[User]: The authenticated User object if the token is valid and the user exists;
                        otherwise, returns None if no token is present.

    Raises:
        HTTPException: If the token is invalid or the user does not exist in the database.
    """
    token = request.cookies.get("admin_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/admin/auth/login"},
        )

    try:
        payload = jwt.decode(
            token, settings.ADMIN_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/admin/auth/login"},
        )

    user = get_admin_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
