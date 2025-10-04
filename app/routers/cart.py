from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.cookies import template_with_cookie
from app.core.exceptions import RedirectHomeException
from app.crud.cart import (
    process_add_to_cart,
    process_remove_from_cart,
    process_update_cart,
    process_view_cart,
)
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.session import get_or_create_session_token
from app.models.user import User
from app.schemas.cart import AddToCartForm, UpdateCartForm

import logging

logger = logging.getLogger(__name__)


router = APIRouter()
templates = Jinja2Templates(directory="app/templates/shop")


@router.get("")
def view_cart(
    request: Request,
    response: Response,
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        cart_summary, subtotal_amount = process_view_cart(
            user=user,
            session_token=session_token,
            db=db,
        )

        response = template_with_cookie(
            user,
            cart_summary,
            subtotal_amount,
            session_token,
            request,
            templates,
        )
    except Exception as e:
        logger.exception(f"Unexpected error in view_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return response


@router.post("/add")
def add_to_cart(
    form: AddToCartForm = Depends(AddToCartForm.as_form),
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        process_add_to_cart(
            sku_id=form.sku_id,
            quantity=form.quantity,
            user=user,
            session_token=session_token,
            db=db,
        )
    except RedirectHomeException as e:
        raise RedirectHomeException("Invalid SKU or other cart error") from e
    except Exception as e:
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return RedirectResponse(url="/cart", status_code=303)


@router.post("/update/{sku_id}")
def update_cart(
    sku_id: int,
    form: UpdateCartForm = Depends(UpdateCartForm.as_form),
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        process_update_cart(
            sku_id=sku_id,
            quantity=form.quantity,
            user=user,
            session_token=session_token,
            db=db,
        )
    except RedirectHomeException as e:
        raise RedirectHomeException("Invalid SKU or other cart error") from e
    except Exception as e:
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return RedirectResponse(url="/cart", status_code=303)


@router.post("/remove/{sku_id}")
def remove_from_cart(
    sku_id: int,
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        process_remove_from_cart(
            sku_id=sku_id,
            user=user,
            session_token=session_token,
            db=db,
        )
    except RedirectHomeException as e:
        raise RedirectHomeException("Invalid SKU or other cart error") from e
    except Exception as e:
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return RedirectResponse(url="/cart", status_code=303)
