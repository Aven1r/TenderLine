from pydantic import BaseModel
from datetime import date, datetime
from backend.api.auth.schemas import User
from enum import Enum

class BudgetSource(str, Enum):
    BUDGET = 'Бюджетные средства'
    NOT_BUDGET = 'Небюджетные средства'
    OMS = 'Средства ОМС'

class Document(BaseModel):
    status: str
    reestr_number: str
    purchase_number: str
    law_number: str
    contract_method: str
    contract_basis: str
    contract_number: str
    contract_lifetime: str
    contract_subject: str
    contract_place: str
    IKZ: str
    budget: BudgetSource
    contract_price: int
    prepayment: int
