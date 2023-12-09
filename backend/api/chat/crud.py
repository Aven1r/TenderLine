from sqlalchemy import select
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import or_

from . import schemas
from .models import Message
from ..documents.models import Document


# async def get_messages(session: AsyncSession, chat_id: int, user_id: int = None, limit: int = 10, skip: int = 0) -> list[Message]:
#     query = select(Message).where(Message.chat_id == chat_id)
#     if user_id:
#         query = query.where(Message.user_id == user_id)
#     rez = await session.execute(query.order_by(Message.created_at).offset(skip).limit(limit))
#     return rez.scalars()
async def create_message(session: AsyncSession, author_id: int, message: schemas.MessageCreate) -> Message:
    message.document = Document(**message.document.model_dump()) if message.document else None
    message_db = Message(**dict(message), author_id=author_id)
    session.add(message_db)
    await session.commit()
    await session.refresh(message_db)
    return message_db


async def get_messages(session: AsyncSession, first_user_id: int, second_user_id: int):
    query = select(Message).where(
        or_(Message.recipient_id == first_user_id and Message.author_id == second_user_id,
        Message.recipient_id == second_user_id and Message.author_id == first_user_id)
    )
    result = await session.execute(query)
    return result.unique().scalars()




# async def get_message(session: AsyncSession, chat_id: int, message_id: int) -> Message:
#     rez = await session.execute(select(Message).where(Message.chat_id == chat_id and Message.id == message_id))
#     return rez.scalar_one_or_none()


# async def create_message(session: AsyncSession, message: schemas.MessageCreate,  user_id: int) -> Message:
#
#     if message.document is not None:
#         message.document = Document(**message.document.model_dump())
#
#     message_db = Message(**dict(message), user_id=user_id, created_at=datetime.now())
#     session.add(message_db)
#     await session.commit()
#     await session.refresh(message_db)
#     return message_db


# async def create_chat(session: AsyncSession, chat: schemas.ChatCreate) -> Chat:
#     chat_dict = chat.model_dump()
#
#     chat_db = Chat(**chat_dict, created_at=datetime.now())
#     session.add(chat_db)
#     await session.commit()
#     await session.refresh(chat_db)
#     return chat_db
#
#
# async def get_chat(session: AsyncSession, user_id: int, recipient_id: int) -> Chat:
#     rez = await session.execute(select(Chat).where(Chat.id == _id))
#     return rez.scalar_one_or_none()
#
#
# async def get_user_chats(session: AsyncSession, user_id: int) -> list[Chat]:
#     rez = await session.execute(select(Chat).where(Chat.consumer_id == user_id or Chat.vendor_id == user_id))
#     return rez.unique().scalars()
