from enum import Enum
from pydantic import BaseModel


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserCreate(BaseModel):
    email: str
    role: Role