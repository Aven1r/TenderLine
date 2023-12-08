from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...auth.models import User


async def get_user_by_id(session: AsyncSession, _id: int) -> User:
    rez = await session.execute(select(User).where(User.id == _id))
    return rez.scalar()


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    rez = await session.execute(select(User).where(User.email == email))
    return rez.scalar()
