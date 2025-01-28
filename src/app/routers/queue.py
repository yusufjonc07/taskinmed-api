from typing import Optional, List  
from app.utils import *
from app.functions.queue import *
from app.functions.income import *
from app.models.queue import *
from app.schemas.queue import *
from app.schemas.income import *
from app.manager import *
from datetime import date as now_date
from datetime import time
from sqlalchemy import Date, cast

queue_router = APIRouter(tags=['Queue Endpoint'])


@queue_router.get("/queues", description="Search servis nomi, bemor ismi va telefoni, doktor ismi bo`yicha")
async def get_queues_list(
    page: int = 1,
    limit: int = 10,
    step: Optional[int] = 0,
    patient_id: Optional[int] = 0,
    search: Optional[str] = '',
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    return get_all_queues(page, limit, usr, db, step, search, patient_id)



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
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):


    if usr.role in ['admin', 'operator', 'reception', 'doctor']:
        for form_data in form_datas:
            create_queue(form_data, p_id, usr, db)
        
        return 'success'
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@queue_router.post("/cashreg/confirm", description="This router is able to add new income and return income id")
async def create_new_income(
    form_data: NewIncome,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_income(form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@queue_router.post("/queue_toggle_skipped", description="This router is able to add new income and return income id")
async def toggle_skipped_func(
    id: int,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        que = db.query(Queue).filter_by(id=id)
        queue = que.first()

        if queue:
            if queue.step == 2:

                que.update({Queue.step: 3, Queue.upt: True})
                db.commit()

                if len(str(queue.room)) == 1:
                    room_path = f"Ovoz 00{queue.room}.wav"
                elif len(str(queue.room)) == 2:
                    room_path = f"Ovoz 0{queue.room}.wav"
                else:
                    room_path = "none"

                if len(str(queue.number)) == 1:
                    pat_path = f"Ovoz 00{queue.number}.wav"
                elif len(str(queue.number)) == 2:
                    pat_path = f"Ovoz 0{queue.number}.wav"
                else:
                    pat_path = "none"

                await manager.queue({
                    "room": queue.room,
                    "number": queue.number,
                    "patient": queue.patient.surename + " " + queue.patient.name,
                    "service": queue.service.name,
                    "track1": pat_path,
                    "track2": "queue.wav",
                    "track3": room_path,
                    "track4": "enter_room.wav"
                })


            elif queue.step == 3:
                que.update({Queue.step: 2, Queue.upt: True})
                db.commit()            
            
            return "sucecss"
                
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@queue_router.get("/queue/goout")
async def goout_patient_queue(
    id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['doctor']:

        next_que = db.query(Queue).filter_by(id=id, step=3)

        next_queue = next_que.first()

        if next_queue:

            next_que.update({Queue.in_room: False, Queue.upt: True})
            db.commit()
            
            return "success"

@queue_router.get("/queue_possibility")
async def get_patient_queue(
    date: str,
    room: int,
    user_id:int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role not in ['any']:

        user = db.query(User).filter_by(id=user_id).first()

        if user:

            if user.queue_time > 0:
                for_one_patient_min = user.queue_time
            else:
                for_one_patient_min = 8

            work_hour = 12
            now = datetime.now()
            from_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
            to_time = now.replace(hour=20, minute=0, second=0, microsecond=0)

            number_of_queues = math.ceil(work_hour * 60 / for_one_patient_min)

            res = []

            for num in range(1, number_of_queues+1):

                next_que = db.query(Queue).filter(
                    Queue.date == date,
                    Queue.step > 0,
                    Queue.step < 4,
                    Queue.room == room,
                    Queue.time >= from_time.strftime("%H:%M:%S"),
                    Queue.time < (from_time + timedelta(minutes=8)).strftime("%H:%M:%S"),
                ).order_by(Queue.id.desc()).first()

                if next_que:
                    poss = False
                else:
                    poss = True


                if date == now.strftime("%Y-%m-%d"):
                    if from_time.strftime("%H:%M") < now.strftime("%H:%M"):
                        poss = False


                res.append({
                    "queue_number": num,
                    "time": from_time.strftime("%H:%M"),
                    "possible": poss
                })

                from_time += timedelta(minutes=for_one_patient_min)

            return res






       


@queue_router.get("/queue/call")
async def call_patient_queue(
    room: int,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['doctor']:

        next_queue = db.query(Queue).filter_by(room=room, step=3).filter(cast(Queue.date,Date) == now_date.today())

        count_of_inrooms = next_queue.filter(Queue.in_room == True).count()

        next_queue = next_queue.filter(Queue.in_room == False).order_by(Queue.number.asc()).first()

        if next_queue and count_of_inrooms < 10:

            db.query(Queue).filter_by(id=next_queue.id).update({Queue.in_room: True, Queue.upt: True})
            db.commit()

            try:
                await manager.queue({
                    "room": next_queue.room,
                    "number": next_queue.number,
                })
                return 'success'
            except Exception as e:
                return 'jonatilmadi' 
            
            


    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

class Confirming(BaseModel):
    queue_id: int
    next_date: Optional[str] = 'none'

@queue_router.post("/diagnosises/confirm")
async def confirm_the_diagnonis(
    form_data: Confirming,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin', 'doctor']:
        confirm_diagnosis(form_data, db)

        
        # if next_que:
        #     await manager.queue({
        #         "room": next_que.room,
        #         "number": next_que.number,
        #         "patient": next_que.patient.surename + " " + next_que.patient.name,
        #         "service": next_que.service.name
        #     })
        return 'success'
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")



@queue_router.post("/queue/complete")
async def complete_queue_finish(
    queue_id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin', 'doctor', 'reception']:
        res = complete_diagnosis_finish(queue_id, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@queue_router.put("/queue/{id}/update", description="This router is able to update queue")
async def update_one_queue(
    id: int,
    form_data: NewQueue,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin', 'operator', 'reception']:
        res = update_queue(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    
@queue_router.put("/queue/{id}/cancel", description="This router is able to cancel queue")
async def cancel_one_queue(
    id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin', 'operator', 'reception', 'casher']:
        res = cancel_queue(id, usr, db)
        if res:
            
            return res

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    