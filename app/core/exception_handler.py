from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.exception import RedirectHomeException
import logging

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="app/templates/admin")


async def shop_redirect_home_handler(request: Request, exc: RedirectHomeException):
    logger.error(f"Redirecting to home due to error: {exc}")
    return RedirectResponse(url="/", status_code=303)


async def admin_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """
    Handles Pydantic validation errors (422 Unprocessable Entity)
    and re-renders the corresponding form with error messages.
    """
    errors = exc.errors()
    form_data = request._form_data if hasattr(request, "_form_data") else {}
    path = request.url.path

    if path.startswith("/admin/products"):
        return templates.TemplateResponse(
            "product_detail.html",
            {
                "request": request,
                "errors": errors,
                "form_data": form_data,
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return templates.TemplateResponse(
        "error/validation_error.html",
        {"request": request, "errors": errors},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
