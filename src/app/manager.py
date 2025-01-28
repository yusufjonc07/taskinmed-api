from typing import List
import inspect
from app.settings import *
from app.auth import get_current_ws_active_user
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def queue(self, message):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

def objToJsonString(self):

    answ = "{"

    for k in sorted(self.__dict__):
        if '_sa_' != k[:4]:
            answ += f"\"{k}\":"

            col = self.__dict__[k]
            
            if type(col).__name__ in ['str', 'datetime', 'time', 'date', 'text']:
                answ += f"\"{col}\","
            elif type(col).__name__ in ['int', 'float', 'int', 'bool']:
                answ += f"{col},"
            else:
                answ += objToJsonString(col)

    answ += "},"

    return answ


def listtostring(data):
    resp_queues = '['
    for item in data:
        resp_queues+=objToJsonString(item)
    resp_queues += ']'

    return resp_queues


