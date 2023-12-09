from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from backend.api.auth.schemas import User
from enum import Enum
from pydantic import EmailStr

class EmailInfo(BaseModel):
    to: EmailStr
    user_name: str
    subject: str
    message: str