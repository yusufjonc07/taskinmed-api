from typing import Optional, List  
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.queue import *
from functions.income import *
from models.queue import *
from schemas.queue import *
from schemas.income import *
from manager import *

queue_router = APIRouter(tags=['Queue Endpoint'])


@queue_router.get("/queues", description="Search servis nomi, bemor ismi va telefoni, doktor ismi bo`yicha")
async def get_queues_list(
    page: int = 1,
    limit: int = 10,
    step: Optional[int] = 0,
    search: Optional[str] = '',
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    return get_all_queues(page, limit, usr, db, step, search)



@queue_router.get("/get_one_queue")
async def get_queues_unit(
    id: int = 1,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    return read_queue(id, usr, db)


@queue_router.post("/queue/create", description="This router is able to add new queue and to return queue id")
async def create_new_queue( 
    p_id: int,
    form_datas: List[NewQueue],
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):


    if usr.role in ['admin', 'operator', 'reception']:
        for form_data in form_datas:
            create_queue(form_data, p_id, usr, db)
        return 'success'
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@queue_router.post("/cashreg/confirm", description="This router is able to add new income and return income id")
async def create_new_income(
    form_data: NewIncome,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_income(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@queue_router.post("/queue_toggle_skipped", description="This router is able to add new income and return income id")
async def toggle_skipped_func(
    id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        que = db.query(Queue).filter_by(id=id)
        queue = que.first()

        if queue:
            if queue.step == 2:

                que.update({Queue.step: 3})
                db.commit()

                if len(str(queue.room)) == 1:
                    room_path = f"Ovoz 00{queue.room}.m4a"
                elif len(str(queue.room)) == 2:
                    room_path = f"Ovoz 0{queue.room}.m4a"
                else:
                    room_path = "none"

                if len(str(queue.number)) == 1:
                    pat_path = f"Ovoz 00{queue.number}.m4a"
                elif len(str(queue.number)) == 2:
                    pat_path = f"Ovoz 0{queue.number}.m4a"
                else:
                    pat_path = "none"

                await manager.queue({
                    "room": queue.room,
                    "number": queue.number,
                    "patient": queue.patient.surename + " " + queue.patient.name,
                    "service": queue.service.name,
                    "track1": pat_path,
                    "track2": "queue.m4a",
                    "track3": room_path,
                    "track4": "enter_room.m4a"
                })


                
                return "success"
            elif queue.step == 3:
                que.update({Queue.step: 2})
                db.commit()
                return "success"

    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@queue_router.get("/queue/call")
async def call_patient_queue(
    id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['doctor']:

        next_que = db.query(Queue).filter_by(id=id, step=3)

        next_queue = next_que.first()

        if next_queue:

            if next_queue.in_room == False:

                next_que.update({Queue.in_room: True})
                db.commit()

                if len(str(next_queue.room)) == 1:
                    room_path = f"Ovoz 00{next_queue.room}.m4a"
                elif len(str(next_queue.room)) == 2:
                    room_path = f"Ovoz 0{next_queue.room}.m4a"
                else:
                    room_path = "none"

                if len(str(next_queue.number)) == 1:
                    pat_path = f"Ovoz 00{next_queue.number}.m4a"
                elif len(str(next_queue.number)) == 2:
                    pat_path = f"Ovoz 0{next_queue.number}.m4a"
                else:
                    pat_path = "none"

                await manager.queue({
                    "room": next_queue.room,
                    "number": next_queue.number,
                    "patient": next_queue.patient.surename + " " + next_queue.patient.name,
                    "service": next_queue.service.name,
                    "track1": pat_path,
                    "track2": "queue.m4a",
                    "track3": room_path,
                    "track4": "enter_room.m4a"
                })
            else:
                next_que.update({Queue.in_room: False})
                db.commit()

            return 'success'

        return 0

    else:
        raise HTTPException(status_code=400, detail="Access denided!")

@queue_router.post("/diagnosises/confirm")
async def confirm_the_diagnonis(
    queue_id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin', 'doctor']:
        confirm_diagnosis(queue_id, db)
        # if next_que:
        #     await manager.queue({
        #         "room": next_que.room,
        #         "number": next_que.number,
        #         "patient": next_que.patient.surename + " " + next_que.patient.name,
        #         "service": next_que.service.name
        #     })
        return 'success'
    else:
        raise HTTPException(status_code=400, detail="Access denided!")



@queue_router.post("/queue/complete")
async def complete_queue_finish(
    queue_id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin', 'doctor']:
        return complete_diagnosis_finish(queue_id, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@queue_router.put("/queue/{id}/update", description="This router is able to update queue")
async def update_one_queue(
    id: int,
    form_data: NewQueue,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin', 'operator', 'reception']:
        return update_queue(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    
@queue_router.put("/queue/{id}/cancel", description="This router is able to cancel queue")
async def cancel_one_queue(
    id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin', 'operator', 'reception']:
        return cancel_queue(id, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    