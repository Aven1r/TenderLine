from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

# from .managers import ConnectionManager, UserConnection
from .managers import ConnectionManager, UserConnection
from .schemas import MessageCreate, Message
from . import crud
from ..dependencies import get_db, get_user
from ..email.routers import email_notify
from ..auth.crud import get_user_by_id


router = APIRouter(
    prefix='/chats',
    tags=['Messages / Chats']
)


@router.get('/messages', response_model=list[Message], dependencies=[Depends(get_user)])
async def get_messages(recipient_id: int, limit: int = 10, skip: int = 0, user=Depends(get_user), db=Depends(get_db)):
    rez = await crud.get_messages(db, user.id, recipient_id)
    return rez

@router.get('/message/{message_id}', response_model=Message)
async def get_message(message_id: int, db=Depends(get_db)):
    return await crud.get_message(db, message_id)


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
            message_schema = {
                'id': message.id,
                'created_at': str(message.created_at),
                'author_id': message.author_id,
                'recipient_id': message.recipient_id,
                'text':message.text,
                'document':message.document.as_dict() if message.document else None
            }
            
            await manager.send_message(user.id, message_schema)
            accepted_by_socket = await manager.send_message(recipient_id, message_schema)
            print(accepted_by_socket)
            
            if not accepted_by_socket:
                pass
                # resipient_user = await get_user_by_id(db, recipient_id)
                # email_notify(resipient_user, 123)

    except WebSocketDisconnect:
        manager.disconnect(user_connection)





