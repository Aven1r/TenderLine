from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas
from .models import Document


async def create_document(session: AsyncSession, document: schemas.DocumentCreate) -> Document:
    ...

