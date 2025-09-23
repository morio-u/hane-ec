from pydantic import BaseModel


class UserCreate(BaseModel):
    last_name: str
    first_name: str
    gender: int
    phone_number: str
    email: str
    password: str
    is_send_newsletter: bool
