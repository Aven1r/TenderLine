from pydantic import BaseModel
from datetime import datetime
from ..auth.schemas import User
from ..documents.schemas import Document, DocumentCreate


class BaseMessage(BaseModel):
    # document: Document
    text: str | None = None


class MessageCreate(BaseMessage):
    recipient_id: int
    document: DocumentCreate | None = None


class Message(BaseMessage):
    id: int
    created_at: datetime
    author_id: int
    recipient_id: int
    document: Document | None = None

    # author: User
    # recipient: User







