from pydantic import BaseModel
from datetime import date, datetime
from backend.api.auth.schemas import User
from enum import Enum

class UserContractInfo(BaseModel):
    company_name: str
    address: str
    phone: str
    checking_account: str
    BIC: str
    INN: str
    KPP: str
    OGRN: str
    OKPO: str
    ОКТМО: str
    email: str

    class Config:
        orm_mode = True