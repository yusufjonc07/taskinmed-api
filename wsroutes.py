from fastapi import APIRouter, WebSocket, Query
from fastapi.responses import HTMLResponse
from db import *
from manager import *
from models.queue import Queue
from models.user import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from functions.queue import get_unpaid_queues
from sqlalchemy import func

# 1

queue_ws = APIRouter()

@queue_ws.websocket("/ws_navbat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await manager.send_personal_message(f"Connected!", websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"closed")
   

@queue_ws.get("/queues/waiting")
async def get_queuegroup_list(db:Session = ActiveSession):

    return db.query(Queue.id, Queue.number, Queue.room).filter_by(
        in_room=False, step=3, date=now_sanavaqt.strftime("%Y-%m-%d")
    ).order_by(Queue.number.asc()).all()

@queue_ws.get("/queues/inroom")
async def get_queueinroom_list(db:Session = ActiveSession):

    return db.query(Queue.id, Queue.number, Queue.room).filter_by(
        in_room=True, step=3, date=now_sanavaqt.strftime("%Y-%m-%d")
    ).order_by(Queue.number.asc()).all()

@queue_ws.get("/queues/skipped")
async def get_queuegroup_skipped(db:Session = ActiveSession):

    return db.query(Queue.id, Queue.number, Queue.room).filter_by(step=2, date=now_sanavaqt.strftime("%Y-%m-%d")).order_by(Queue.id.asc()).all()