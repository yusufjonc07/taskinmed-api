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

queue_ws = APIRouter()

@queue_ws.websocket("/ws_navbat")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


@queue_ws.get("/queues/waiting")
async def get_queuegroup_list(db:Session = ActiveSession):

    return db.query(
        func.min(Queue.number).label("num"), Queue.room
    ).filter_by(
        step=3, date=now_sanavaqt.strftime("%Y-%m-%d")
    ).group_by(Queue.room).order_by(Queue.number.asc()).all()

@queue_ws.get("/queues/skipped")
async def get_queuegroup_skipped(db:Session = ActiveSession):

    return db.query(Queue.number, Queue.room).filter_by(step=2, date=now_sanavaqt.strftime("%Y-%m-%d")).order_by(Queue.id.asc()).all()