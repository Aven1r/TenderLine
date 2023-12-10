from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_user
from ..auth.schemas import User
from .api import schemas
from .api import crud

router = APIRouter(tags=["profile"], prefix='/profile')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_profile(current_user: User=Depends(get_user), db=Depends(get_db)):
    user_info = await crud.get_user_full_info(db, current_user.id)
    print(user_info)
    print(":dddddd\n\n\n\n")
    print(user_info)
    print(":dddddd\n\n\n\n")
    print(user_info)
    return user_info
    

@router.post('/update', status_code=status.HTTP_200_OK)
async def update_profile(user: schemas.UserContractInfo, current_user: User=Depends(get_user), db=Depends(get_db)):
    return crud.update_user_info(db, user, current_user.id)