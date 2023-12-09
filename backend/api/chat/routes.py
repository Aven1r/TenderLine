from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

# from .managers import ConnectionManager, UserConnection
from .managers import ConnectionManager, UserConnection
from .schemas import MessageCreate, Message
from . import crud
from ..dependencies import get_db, get_user


router = APIRouter(
    prefix='/chats',
    tags=['Messages / Chats']
)


@router.get('/messages', response_model=list[Message], dependencies=[Depends(get_user)])
async def get_messages(recipient_id: int, limit: int = 10, skip: int = 0, user=Depends(get_user), db=Depends(get_db)):
    rez = await crud.get_messages(db, user.id, recipient_id)
    return rez


@router.post('/messages/create', response_model=Message, dependencies=[Depends(get_user)])
async def create_message(message: MessageCreate, user=Depends(get_user),  db=Depends(get_db)):
    return await crud.create_message(db, user.id, message)


manager = ConnectionManager()


@router.websocket('/ws/{recipient_id}')
async def websocket_chat_endpoint(websocket: WebSocket, recipient_id: int, user=Depends(get_user), db=Depends(get_db)):
    print(user.id, recipient_id)
    user_connection = UserConnection(user.id, websocket)
    await manager.connect(user_connection)
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            message = await crud.create_message(db, user.id, MessageCreate(**data, recipient_id=recipient_id))

            accepted_by_socket = await manager.send_message(recipient_id, message)
    except WebSocketDisconnect:
        manager.disconnect(user_connection)





