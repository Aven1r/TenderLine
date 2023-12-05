from pydantic import BaseModel
from datetime import datetime
from ..documents.schemas import Document
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
    comment: str | None = None


class MessageCreate(BaseMessage):
    chat_id: int



class Message(BaseMessage):
    id: int
    created_at: datetime
    chat: Chat







