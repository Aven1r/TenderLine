from starlette.websockets import WebSocket
from .schemas import  Message
from ..auth.schemas import User
from dataclasses import dataclass
import json


@dataclass
class UserConnection:
    user_id: int
    websocket: WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: list[UserConnection] = []

    async def connect(self, connection: UserConnection):
        for con in self.active_connections:
            if con.user_id == connection.user_id:
                self.active_connections.remove(con)

        await connection.websocket.accept()
        self.active_connections.append(connection)
        print(self.active_connections)

    def disconnect(self, connection: UserConnection):
        self.active_connections.remove(connection)

    async def send_message(self, recipient_id: int, message) -> bool:
        for connection in self.active_connections:
            if connection.user_id == recipient_id:
                await connection.websocket.send_json(json.dumps(message))
                return True
        return False

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.websocket.send_text(message)


