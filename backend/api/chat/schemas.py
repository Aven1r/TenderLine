from pydantic import BaseModel
from datetime import datetime


class BaseChat(BaseModel):
    pass


class ChatCreate(BaseChat):
    pass


class Chat(BaseModel):
    id: int


class BaseMessage(BaseModel):
    pass


class MessageCreate(BaseMessage):
    pass


class Message(BaseMessage):
    id: int
    chat: Chat
    datetime: datetime


class DokumentBlock(BaseModel):
    id: int
    title: str
    text: str


class Dokument(BaseModel):
    id: int
    customer: User
    ...

    body: list[DokumentBlock]


"зочу купить у ______товар "