from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal
from .auth.secure import verify_jwt_token
from .auth import crud
from .auth.schemas import User


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def get_user(access_token: str = Cookie(None), db=Depends(get_db)) -> User | None:
    payload = verify_jwt_token(access_token)
    user = await crud.get_user_by_id(db, payload.get('sub'))
    return user
