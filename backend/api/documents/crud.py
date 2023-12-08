# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from . import schemas
# # from .models import Document
# # from ..chat.models import Chat
#
#
# async def create_document(session: AsyncSession, document: schemas.DocumentCreate) -> Document:
#     document_db = Document(**document.model_dump())
#     session.add(document_db)
#     await session.commit()
#     await session.refresh(document_db)
#     return document_db
#
#
# async def get_document_by_message_id(session: AsyncSession, _id: int) -> Document | None:
#     query = select(Document).where(Document.message_id == _id)
#     rez = await session.execute(query)
#     return rez.scalar_one_or_none()
#
#
# async def get_document_history(session: AsyncSession, consumer_id: int, supplier_id: int) -> list[Document]:
#     query = select(Document).where(Document.consumer_id == consumer_id and Document.supplier_id == supplier_id)
#     rez = await session.execute(query)
#     return rez.unique().scalars()
