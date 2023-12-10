from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...auth.models import User, UserContractInfo
from .schemas import UserContractInfo as UserContractInfoSchema


async def get_user_full_info(session: AsyncSession, _id: int):
    stmt = select(UserContractInfo).where(User.id == _id)
    rez = await session.execute(stmt)
    return rez.scalar()


async def update_user_info(session: AsyncSession, user: UserContractInfoSchema, _id: int):
    stmt = select(UserContractInfo).where(User.id == _id)
    rez = await session.execute(stmt)
    user_db = rez.scalar_one_or_none()
    user_db.name = user.name
    user_db.email = user.email
    user_db.phone = user.phone
    user_db.address = user.address
    user_db.company_name = user.company_name
    user_db.checking_account = user.checking_account
    user_db.BIC = user.BIC
    user_db.INN = user.INN
    user_db.KPP = user.KPP
    user_db.OGRN = user.OGRN
    user_db.OKPO = user.OKPO
    user_db.ОКТМО = user.ОКТМО


    await session.commit()
    return user_db
