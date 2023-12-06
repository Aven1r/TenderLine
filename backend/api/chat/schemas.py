from pydantic import BaseModel
from datetime import datetime
from ..documents.schemas import Document, DocumentCreate
from ..auth.schemas import User


class BaseChat(BaseModel):
    pass


class ChatCreate(BaseChat):
    vendor_id: int
    consumer_id: int


class Chat(BaseChat):
    id: int
    created_at: datetime
    vendor: User
    consumer: User


class BaseMessage(BaseModel):
    # document: Document
    text: str | None = None


class MessageCreate(BaseMessage):
    chat_id: int
    document_id: int | None



class Message(BaseMessage):
    id: int
    created_at: datetime
    chat: Chat
    document: Document | None = None






