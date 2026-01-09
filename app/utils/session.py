import uuid


def generate_session_token() -> str:
    """
    Generates a new unique session token.

    Returns:
        str: A UUID-based session token as a string.
    """
    return str(uuid.uuid4())
