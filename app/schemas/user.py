from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    last_name: str
    middle_name: Optional[str] = None
    first_name: str
    gender: int
    phone_number: str
    email: str
    password: str
    is_send_newsletter: bool