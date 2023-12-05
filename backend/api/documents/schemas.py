from pydantic import BaseModel
from datetime import date
from backend.api.auth.schemas import User


class BaseDocumentField(BaseModel):
    name: str
    description: str
    text: str
    comment: str | None = None


class CreateDocumentField(BaseDocumentField):
    pass


class DocumentField(BaseDocumentField):
    id: int
    is_changed: bool = False


class BaseDocument(BaseModel):
    customer: User
    supplier: User

    field1: BaseDocumentField
    field2: BaseDocumentField
    field3: BaseDocumentField
    field4: BaseDocumentField


class DocumentCreate(BaseDocument):
    pass


class Document(BaseDocument):
    id: int

    conclusion_at: date

    field1: DocumentField
    field2: DocumentField
    field3: DocumentField
    field4: DocumentField
