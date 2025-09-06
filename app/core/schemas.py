from pydantic import BaseModel

class OAuth2PasswordRequestLoginForm(BaseModel):
    email: str
    password: str