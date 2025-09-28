from typing import Optional
import uuid


def generate_session_token() -> str:
    """
    Generates a new unique session token.

    Returns:
        str: A UUID-based session token as a string.
    """
    return str(uuid.uuid4())


def get_or_create_session_token(session_token: Optional[str]) -> str:
    """
    Returns the given session token if it exists and is truthy;
    otherwise, generates and returns a new session token.

    Args:
        session_token (Optional[str]): An existing session token, or None/empty if not available.

    Returns:
        str: The original session token if valid, or a newly generated session token.
    """
    return session_token or generate_session_token()
