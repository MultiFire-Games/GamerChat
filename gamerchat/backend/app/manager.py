from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users = {}

    async def connect(self, websocket: WebSocket, nick: str):
        self.active_connections.append(websocket)
        self.users[websocket] = nick
        await self.broadcast_user_list()

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if websocket in self.users:
            del self.users[websocket]

    async def broadcast_message(self, sender_nick: str, message: str):
        for connection in self.active_connections:
            await connection.send_json({
                'type': 'chat_message',
                'nick': sender_nick,
                'message': message
            })

    async def broadcast_user_list(self):
        users = list(self.users.values())
        for connection in self.active_connections:
            await connection.send_json({
                'type': 'user_list',
                'users': users
            })
