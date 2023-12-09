from pydantic import BaseModel
from datetime import datetime
from ..auth.schemas import User
from ..documents.schemas import Document


class BaseMessage(BaseModel):
    # document: Document
    text: str | None = None
    document: Document | None = None


class MessageCreate(BaseMessage):
    recipient_id: int


class Message(BaseMessage):
    id: int
    created_at: datetime
    author_id: int
    recipient_id: int
    # author: User
    # recipient: User







