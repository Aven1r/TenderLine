from sqlalchemy import select
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas
from .models import Chat, Message


async def get_messages(session: AsyncSession, chat_id: int, user_id: int = None, limit: int = 10, skip: int = 0) -> list[Message]:
    query = select(Message).where(Message.chat_id == chat_id)
    if user_id:
        query = query.where(Message.user_id == user_id)
    rez = await session.execute(query.order_by(Message.created_at).offset(skip).limit(limit))
    return rez.scalars()


async def get_message(session: AsyncSession, chat_id: int, message_id: int) -> Message:
    rez = await session.execute(select(Message).where(Message.chat_id == chat_id, Message.id == message_id))
    return rez.scalar_one_or_none()


async def create_message(session: AsyncSession, message: schemas.MessageCreate, user_id: int) -> Message:
    message_db = Message(**message.model_dump(), user_id=user_id, created_at=datetime.now())
    session.add(message_db)
    await session.commit()
    await session.refresh(message_db)
    print(message_db)
    return message_db


async def create_chat(session: AsyncSession, chat: schemas.ChatCreate) -> Chat:
    chat_dict = chat.model_dump()

    chat_db = Chat(**chat_dict, created_at=datetime.now())
    session.add(chat_db)
    await session.commit()
    await session.refresh(chat_db)
    return chat_db


async def get_chat(session: AsyncSession, _id: int) -> Chat:
    rez = await session.execute(select(Chat).where(Chat.id == _id))
    return rez.scalar_one_or_none()
