from pydantic import BaseModel
from datetime import date, datetime
from backend.api.auth.schemas import User
from enum import Enum


class BudgetSource(str, Enum):
    BUDGET = 'Бюджетные средства'
    NOT_BUDGET = 'Небюджетные средства'
    OMS = 'Средства ОМС'


class DocumentStatus(str, Enum):
    CONFIRMED = 'Подтверждено'
    EDITED = 'Отредактировано'
    REJECTED = 'Отклонено'
    CREATED = 'Создано'
    

class BaseDocument(BaseModel):
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
    contract_price: str
    prepayment: str
    
    previous_document_id: int | None = None
    document_status: DocumentStatus = DocumentStatus.CREATED
    
    class Config:
        use_enum_values = True


class DocumentCreate(BaseDocument):
    pass


class Document(BaseDocument):
    id: int
    
    class Config:
        use_enum_values = True
