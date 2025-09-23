from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from app.dependencies.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "disabled": current_user["disabled"]}
