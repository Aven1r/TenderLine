from fastapi import APIRouter, Depends, Form, Cookie
from starlette.responses import JSONResponse
from .secure import create_access_token, verify_jwt_token, verify_password, get_password_hash
from .schemas import CreateUser, User
from ..dependencies import get_db
from ..dependencies import get_user as get_current_user
from . import crud

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register', response_model=User)
async def register_user(user: CreateUser, db=Depends(get_db)):
    user.password = get_password_hash(user.password)
    db_user = await crud.create_user(db, user)
    return db_user


@router.post('/login')
async def login_user(email: str = Form(), password: str = Form(), db=Depends(get_db)):
    user = await crud.get_user_by_email(db, email)

    if not user:
        return 0

    if not verify_password(password, user.password):
        return 1

    token = create_access_token({'sub': user.id, 'name': user.name})

    response = JSONResponse(status_code=200, content={"data": "ACCEPT"})
    response.set_cookie(key="access_token", value=token)
    return response


@router.post('/logout')
async def logout_user():
    response = JSONResponse(status_code=200, content={"data": "LOGOUT"})
    response.delete_cookie(key="access_token")
    return response


@router.get('/user/{user_id}', response_model=User | None)
async def get_user(user_id, db=Depends(get_db)):
    return await crud.get_user_by_id(db, user_id)


@router.get('/users', response_model=list[User])
async def get_users(user=Depends(get_current_user), db=Depends(get_db)):
    return await crud.get_all_users(db, user.id)


@router.get('/test')
async def test(current_user:User=Depends(get_current_user)):
    return current_user
