    
from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.queue import *
from models.queue import *
from schemas.queue import *
from manager import *

queue_router = APIRouter(tags=['Queue Endpoint'])


@queue_router.get("/queues", description="This router returns list of the queues using pagination")
async def get_queues_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_queues(page, limit, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")



@queue_router.post("/queue/create", description="This router is able to add new queue and return queue id")
async def create_new_queue(
    p_id: int,
    form_data: NewQueue,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_queue(form_data, p_id, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@queue_router.put("/queue/{id}/update", description="This router is able to update queue")
async def update_one_queue(
    id: int,
    form_data: NewQueue,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_queue(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    