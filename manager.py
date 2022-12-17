from typing import List
import inspect
import settings
from auth import get_current_ws_active_user
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, token, db, websocket: WebSocket):
        await websocket.accept()
        
        self.active_connections.append(websocket)
       
        
    async def disconnect(self, appending: WebSocket):
        self.active_connections.remove(appending)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def sendtocash(self, data):
        for connection in self.active_connections:
            await connection.send_json(data)


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


