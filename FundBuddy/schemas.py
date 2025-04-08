from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    email: Optional[str] = None
