from typing import List, Optional
from fastapi import Request, Cookie
from app.utils.session import generate_session_token


def get_or_create_session_token(session_token: Optional[str] = Cookie(None)) -> str:
    """
    Retrieve the provided session token from cookies if available and non-empty;
    otherwise, generate and return a new session token.

    This function is intended to be used as a FastAPI dependency.

    Args:
        session_token (Optional[str]): The session token obtained from the client's cookies,
                                       or None/empty string if not provided.

    Returns:
        str: A valid session token — either the one from the cookie or a newly generated token.
    """
    return session_token or generate_session_token()


def get_errors_from_session(request: Request) -> Optional[List[str]]:
    """
    Retrieve and remove error messages from the user's session.

    Args:
        request (Request): The current HTTP request object containing the session.

    Returns:
        Optional[List[str]]: A list of error messages if present, otherwise None.
    """
    return request.session.pop("errors", None)
