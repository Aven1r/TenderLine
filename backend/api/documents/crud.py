from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas
from .models import Document


async def create_document(session: AsyncSession, document: schemas.DocumentCreate) -> Document:
    document_db = Document(**document.model_dump())
    session.add(document_db)
    await session.commit()
    await session.refresh(document_db)
    return document_db

