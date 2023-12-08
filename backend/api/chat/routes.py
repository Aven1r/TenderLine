from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from .managers import ConnectionManager, UserConnection
from .schemas import MessageCreate, ChatCreate, Message, Chat
from . import crud
from ..auth.schemas import User
from ..documents.schemas import DocumentCreate
from ..dependencies import get_db, get_user

router = APIRouter(
    prefix='/chats',
    tags=['Messages / Chats']
)


@router.get('/', dependencies=[Depends(get_user)])
async def get_chats(user_id: int = None):
    pass


@router.post('/create', response_model=Chat, dependencies=[Depends(get_user)])
async def create_chat(chat: ChatCreate, db=Depends(get_db)):
    chat_db = await crud.create_chat(db, chat)
    return chat_db


@router.get('/{chat_id}', response_model=Chat | None, dependencies=[Depends(get_user)])
async def get_chat(chat_id: int, db=Depends(get_db)):
    return await crud.get_chat(db, chat_id)


@router.get('/{chat_id}/messages', response_model=list[Message], dependencies=[Depends(get_user)])
async def get_messages(chat_id: int, limit: int = 10, skip: int = 0, db=Depends(get_db)):
    return await crud.get_messages(db, chat_id, None, skip=skip, limit=limit)


@router.get('/{chat_id}/messages/{message_id}', response_model=Message | None, dependencies=[Depends(get_user)])
async def get_message(chat_id: int, message_id: int,  db=Depends(get_db)):
    return await crud.get_message(db, chat_id, message_id)


@router.post('/{chat_id}/messages/create', response_model=Message, dependencies=[Depends(get_user)])
async def create_message(chat_id: int, message: MessageCreate,  db=Depends(get_db)):
    return await crud.create_message(db, message, chat_id)

manager = ConnectionManager()


@router.websocket('/ws/chat/{chat_id}')
async def websocket_chat_endpoint(websocket: WebSocket, chat_id: int, user=Depends(get_user), db=Depends(get_db)):
    chat = await crud.get_chat(db, chat_id)
    recipient = chat.vendor if user != chat.vendor else chat.consumer
    user_connection = UserConnection(chat, user, websocket)
    await manager.connect(user_connection)
    try:
        while True:
            data = await websocket.receive_json()

            message = await crud.create_message(db, MessageCreate(**data), user.id)
            await manager.send_message(recipient, message)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_connection)
        # await manager.broadcast(f"Client #{client_id} left the chat")
