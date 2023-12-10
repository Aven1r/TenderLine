from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas
from .models import User
from .models import UserContractInfo


async def create_user(session: AsyncSession, user: schemas.CreateUser) -> User:
    db_user = User(**user.model_dump())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    db_user_contract_info = UserContractInfo(user_id=db_user.id)
    session.add(db_user_contract_info)
    await session.commit()
    return db_user


async def get_all_users(session: AsyncSession, exclude_user_id: int | None = None) -> list[User]:
    query = select(User)
    if exclude_user_id is not None:
        query = query.where(User.id != exclude_user_id)
    rez = await session.execute(query)
    return rez.unique().scalars()


async def get_user_by_id(session: AsyncSession, _id: int) -> User:
    rez = await session.execute(select(User).where(User.id == _id))
    return rez.scalar()


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    rez = await session.execute(select(User).where(User.email == email))
    return rez.scalar()
