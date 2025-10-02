from decimal import Decimal
from typing import Any, List, Dict
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.models.user import User


def set_template_response(
    user: User,
    cart_summary: List[Dict[str, Any]],
    subtotal_amount: Decimal,
    request: Request,
    templates: Jinja2Templates,
) -> Response:
    """
    Render and return the cart template response.

    Args:
        user (User): Logged-in user.
        cart_summary (List[Dict[str, Any]]): Summary of cart items.
        subtotal_amount (Decimal): Cart subtotal amount.
        request (Request): FastAPI request object.
        templates (Jinja2Templates): Jinja2 template engine.

    Returns:
        Response: HTML response for the cart page.
    """
    response = templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "user": user,
            "cart_summary": cart_summary,
            "subtotal_amount": subtotal_amount,
        },
    )

    return response


def set_session_cookie(session_token: str, response: Response) -> Response:
    """
    Set the session token as an HTTP-only cookie in the response.

    Args:
        session_token (str): Session token to store.
        response (Response): Response object to attach the cookie to.

    Returns:
        Response: Response with session cookie set.
    """
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS,
    )

    return response


def template_with_cookie(
    user: User,
    cart_summary: List[Dict[str, Any]],
    subtotal_amount: Decimal,
    session_token: str,
    request: Request,
    templates: Jinja2Templates,
) -> Response:
    """
    Render the cart template and set the session cookie.

    Args:
        user (User): Logged-in user.
        cart_summary (List[Dict[str, Any]]): Summary of cart items.
        subtotal_amount (Decimal): Cart subtotal amount.
        session_token (str): Session token to store.
        request (Request): FastAPI request object.
        templates (Jinja2Templates): Jinja2 template engine.

    Returns:
        Response: HTML response with session cookie set.
    """
    response = set_template_response(
        user, cart_summary, subtotal_amount, request, templates
    )

    return set_session_cookie(session_token, response)


def redirect_with_cookie(session_token: str) -> Response:
    """
    Return a redirect response with the session cookie set.

    Args:
        session_token (str): Session token to store.

    Returns:
        Response: Redirect response to the cart page with cookie set.
    """
    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=settings.SESSION_TOKEN_EXPIRE_SECONDS,
    )

    return response
