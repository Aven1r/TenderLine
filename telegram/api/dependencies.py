from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db():
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()