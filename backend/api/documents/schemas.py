# from pydantic import BaseModel
# from datetime import date, datetime
# from backend.api.auth.schemas import User
#
#
# class BaseDocumentField(BaseModel):
#     description: str
#     value: str
#
#
# class CreateDocumentField(BaseDocumentField):
#     pass
#
#
# class DocumentField(BaseDocumentField):
#     id: int
#     is_changed: bool = False
#
#
# class BaseDocument(BaseModel):
#     pass
#
#     # field1: BaseDocumentField
#     # field2: BaseDocumentField
#     # field3: BaseDocumentField
#     # field4: BaseDocumentField
#
#
# class DocumentCreate(BaseDocument):
#     previous_document_id: int | None
#     supplier_id: int
#     consumer_id: int
#
#
# class Document(BaseDocument):
#     id: int
#     supplier_id: int
#     consumer_id: int
#     created_at: datetime
#
#     fields: list[DocumentField]
#     # field1: DocumentField
#     # field2: DocumentField
#     # field3: DocumentField
#     # field4: DocumentField
