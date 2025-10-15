from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.cookie import template_with_cookie
from app.core.exception import RedirectHomeException
from app.crud.shop.cart import (
    process_remove_from_cart,
    process_update_cart,
    process_view_cart,
)
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.session import (
    get_errors_from_session,
    get_or_create_session_token,
)
from app.models.shop import User
from app.schemas.shop.cart import UpdateCartForm

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
    errors: Optional[list[str]] = Depends(get_errors_from_session),
) -> Response:
    try:
        # Retrieve and prepare the user's cart data for display, including cart summary and subtotal.
        cart_summary, subtotal_amount = process_view_cart(
            user=user,
            session_token=session_token,
            db=db,
        )

        # Render the cart template and set the session cookie.
        response = template_with_cookie(
            user,
            cart_summary,
            subtotal_amount,
            session_token,
            request,
            templates,
            errors,
        )
    except Exception as e:
        logger.exception(f"Unexpected error in view_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return response


@router.post("/update/{sku_id}")
def update_cart(
    sku_id: int,
    form: UpdateCartForm = Depends(UpdateCartForm.as_form),
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
) -> RedirectResponse:
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        # Update the quantity of an existing cart item in the user's cart.
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
        # For traceback
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return RedirectResponse(url="/cart", status_code=303)


@router.post("/remove/{sku_id}")
def remove_from_cart(
    sku_id: int,
    session_token: str = Depends(get_or_create_session_token),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
) -> RedirectResponse:
    # TODO: Add validation, Get Product's price etc.. from DB, Caliculate Tax

    try:
        # Remove a SKU from the user's cart.
        process_remove_from_cart(
            sku_id=sku_id,
            user=user,
            session_token=session_token,
            db=db,
        )
    except RedirectHomeException as e:
        raise RedirectHomeException("Invalid SKU or other cart error") from e
    except Exception as e:
        # For traceback
        logger.exception(f"Unexpected error in add_to_cart: {e}")
        raise RedirectHomeException("Unexpected error")

    return RedirectResponse(url="/cart", status_code=303)
