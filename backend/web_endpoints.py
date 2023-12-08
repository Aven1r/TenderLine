from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates
from .api.auth.crud import get_all_users
from backend.api.dependencies import get_user, get_db

router = APIRouter(
    prefix='/web',
    tags=['Web']
)

templates = Jinja2Templates(directory="frontend/templates")


@router.get('/chat')
async def view_chat(request: Request, user=Depends(get_user), db=Depends(get_db)):
    chats = await get_all_users(db, user.id)
    return templates.TemplateResponse("index.html", {'request': request, 'user_id': user.id, 'chats': chats})

