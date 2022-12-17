from fastapi import APIRouter, WebSocket, Query
from db import *
from manager import *
from models.queue import Queue
from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from functions.queue import get_unpaid_queues
import time
import threading
queue_ws = APIRouter()



@queue_ws.websocket("/unpaid_queues")
async def ws_unpaid_queues(
    websocket: WebSocket,
    token: str = Query(...), 
    db:Session = ActiveSession,
):

    user = get_current_ws_active_user(token, db)
    if user:
        await manager.connect(token, db, websocket)
            # while 1 == 1:
        queuses = get_unpaid_queues(db)
        resp_queues = listtostring(queuses)

        await websocket.send_json(resp_queues)


    #     #
    #     # print(resp_queues)
    #     # await websocket.send_json(resp_queues)
        

