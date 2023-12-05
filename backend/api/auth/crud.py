from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas
from .models import User


async def create_user(session: AsyncSession, user: schemas.CreateUser) -> User:
    db_user = User(**user.model_dump())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_id(session: AsyncSession, _id: int) -> User:
    rez = await session.execute(select(User).where(User.id == _id))
    return rez.scalar()


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    rez = await session.execute(select(User).where(User.email == email))
    return rez.scalar()
