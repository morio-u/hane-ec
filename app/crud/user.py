from app.core.security import get_password_hash, verify_password

# Provisional information for development
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": get_password_hash("secret"),
        "disabled": False,
    }
}

def get_user_by_username(username: str):
    user_dict = fake_users_db.get(username)
    return user_dict

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user
