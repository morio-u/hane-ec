from fastapi.responses import RedirectResponse
from fastapi import Request
from app.core.exceptions import RedirectHomeException
import logging

logger = logging.getLogger(__name__)


async def redirect_home_handler(request: Request, exc: RedirectHomeException):
    logger.error(f"Redirecting to home due to error: {exc}")
    return RedirectResponse(url="/", status_code=303)
