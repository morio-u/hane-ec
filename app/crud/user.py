from app.core.security import get_password_hash, verify_password

# Provisional information for development
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": get_password_hash("secret"),
        "disabled": False,
    }
}

async def get_user_by_username(username: str):
    return fake_users_db.get(username)

async def authenticate_user(username: str, password: str):
    """
    Asynchronous user authentication function
    Ensure it can be called with await even when replaced in the database
    """
    user = await get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

async def create_user(username: str, password: str):
    """
    Create a new user and save into fake_users_db
    """
    if username in fake_users_db:
        return None
    hashed_pw = get_password_hash(password)
    fake_users_db[username] = {
        "username": username,
        "hashed_password": hashed_pw,
        "disabled": False,
    }
    return fake_users_db[username]