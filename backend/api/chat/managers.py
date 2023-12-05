from starlette.websockets import WebSocket
from .schemas import Chat, Message
from ..auth.schemas import User
from dataclasses import dataclass


@dataclass
class UserConnection:
    chat: Chat
    user: User
    websocket: WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: list[UserConnection] = []

    async def connect(self, connection: UserConnection):
        await connection.websocket.accept()
        self.active_connections.append(connection)

    def disconnect(self, connection: UserConnection):
        self.active_connections.remove(connection)

    async def send_message(self, recipient: User, message: Message):
        for connection in self.active_connections:
            if connection.user == recipient:
                await connection.websocket.send_json(message.model_dump())

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.websocket.send_text(message)


