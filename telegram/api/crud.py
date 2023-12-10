from .dependencies import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from passlib.context import CryptContext
from fastapi import Depends

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_email(email: str) -> User:
    async with get_db() as session:
        stmt = select(User).where(User.email == email)
        rez = await session.execute(stmt)
        return rez.scalar_one_or_none()
    

async def get_name_by_email(email: str) -> str:
    async with get_db() as session:
        stmt = select(User).where(User.email == email)
        rez = await session.execute(stmt)
        return rez.scalar_one().name


async def compare_password(password: str) -> bool:
    async with get_db() as session:
        stmt = select(User).where(User.password == password)
        rez = await session.execute(stmt)
        itog = rez.scalar_one_or_none()
        if itog == None:
            return False
        else:
            return True
        
async def put_id_to_db(id, email):
    async with get_db() as session:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            user.telegram_id = id
            await session.commit()
        


    