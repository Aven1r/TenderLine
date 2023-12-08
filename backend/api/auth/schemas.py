from pydantic import BaseModel, EmailStr
from enum import Enum


class UserStatus(str, Enum):
    CONSUMER = 'CON'
    SUPPLIER = 'SUP'
    COMBO = 'COM'


class BaseUser(BaseModel):
    name: str
    address: str
    email: EmailStr
    status: UserStatus
    password: str

    class Config:
        use_enum_values = True


class CreateUser(BaseUser):
    pass


class User(BaseUser):
    id: int
    use_email_notification: bool = True


