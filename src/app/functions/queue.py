    
from fastapi import HTTPException
from app.models.queue import Queue, now_sanavaqt
from sqlalchemy.orm import joinedload
from app.models.service import Service
from app.models.user import User
from app.models.doctor import Doctor
from app.models.setting import Setting
from app.models.income import Income
from app.models.diagnosis import Diagnosis
from app.models.recall import Recall
from app.models.recipe import Recipe
from app.models.patient import Patient, now_sanavaqt
from app.manager import *
from sqlalchemy import or_, func
from sqlalchemy.orm import Session
import math
from app.trlatin import tarjima
from datetime import timedelta, datetime
from .request import insert_req


def get_count_queues(usr, db):

    return db.query(Queue).count()


def get_all_queues(page, limit, usr, db, step, search, patient_id):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    qs = db.query(Queue) \
        .join(Queue.service) \
        .join(Queue.patient) \
        .join(Queue.doctor) \
        .join(Doctor.user) \
        .options(
            joinedload(Queue.doctor).subqueryload(Doctor.user).load_only(
                User.name,
                User.phone,
            ),
            joinedload(Queue.patient),
            joinedload(Queue.service),
            joinedload(Queue.diagnosiss) \
            .subqueryload(Diagnosis.recipes) \
            .subqueryload(Recipe.drug),
        )

    if usr.role == 'doctor':
        qs = qs.filter(Queue.doctor.has(user_id=usr.id))

    if len(search) > 0:
        qs = qs.filter(
            or_(
                Service.name.like(f"%{tarjima(search, 'uz')}%"),
                Service.name.like(f"%{tarjima(search, 'ru')}%"),
                Patient.name.like(f"%{tarjima(search, 'uz')}%"),
                Patient.name.like(f"%{tarjima(search, 'ru')}%"),
                Patient.phone.like(f"%{tarjima(search, 'uz')}%"),
                Patient.phone.like(f"%{tarjima(search, 'ru')}%"),
                User.name.like(f"%{tarjima(search, 'uz')}%"),
                User.name.like(f"%{tarjima(search, 'ru')}%"),
            )       
        )

    if patient_id > 0:
        qs = qs.filter(Queue.patient_id==patient_id).order_by(Queue.id.desc())
    else:
        qs = qs.filter(Queue.step==step, Queue.date == datetime.now().strftime("%Y-%m-%d")).order_by(Queue.number.asc())

    data = qs.offset(offset).limit(limit)

    return {
        "data": data.all(),
        "count": math.ceil(data.count() / limit),
        "page": page,
        "limit": limit,
    }

def read_queue(id, usr, db: Session):

    

    this_queue = db.query(Queue) \
        .join(Queue.service) \
        .join(Queue.patient) \
        .join(Queue.doctor) \
        .join(Doctor.user) \
        .options(
            joinedload(Queue.doctor).subqueryload(Doctor.user).load_only(
                User.name,
                User.phone,
            ),
            joinedload(Queue.patient),
            joinedload(Queue.service),
            joinedload(Queue.diagnosiss) \
            .subqueryload(Diagnosis.recipes) \
            .subqueryload(Recipe.drug),
        ).filter(Queue.id == id).first()
    

    if this_queue:
        queue_count = db.query(Queue).filter(Queue.doctor_id == this_queue.doctor_id, Queue.step > 0, Queue.patient_id==this_queue.patient_id).count()
        this_queue.queue_count = queue_count
        return this_queue
    else:
        raise HTTPException(status_code=400, detail="Queue topilmadi!")


def create_queue(form_data, p_id, usr, db):

    try:

        new_queue = Queue(
            room=form_data.room,
            doctor_id=form_data.doctor_id,
            service_id=form_data.service_id,
            time=form_data.time,
            date=form_data.date,
            complaint=form_data.complaint,
            responsible=form_data.responsible,
            treatment=form_data.treatment,
            patient_id=p_id,
            user_id=usr.id,
            number=form_data.number
        )

        db.add(new_queue)
        db.commit()
        
        return 'success'
    except Exception as e:
        print(e)

def get_unpaid_queues(db):
    return db.query(Queue).options(
            joinedload(Queue.doctor).subqueryload(Doctor.user).load_only(
                User.name,
                User.phone,
            ),
            joinedload(Queue.patient),
            joinedload(Queue.service),
            joinedload(Queue.diagnosiss) \
            .subqueryload(Diagnosis.recipes) \
            .subqueryload(Recipe.drug),
        ).filter_by(step=1).order_by(Queue.id.desc()).all()

def update_queue(id, form_data, usr, db):

    this_queue = db.query(Queue).filter(Queue.id == id)

    if this_queue.first():

        this_queue.update({
            Queue.doctor_id: form_data.doctor_id,
            Queue.service_id: form_data.service_id,
            Queue.room: form_data.room,
            Queue.time: form_data.time,
            Queue.number: form_data.number,
            Queue.complaint:form_data.complaint,
            Queue.responsible:form_data.responsible,
            Queue.treatment:form_data.treatment,
            Queue.date: form_data.date,
            Queue.upt: True,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Queue topilmadi!")

def confirm_queue(usr, id, db):

    this_queue = db.query(Queue).filter_by(id=id, step=2)

    if this_queue.first():

        this_queue.update({Queue.step: 3, Queue.upt: True,})
        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Navbat topilmadi!")

def confirm_diagnosis(form_data, db):

    this_queue = db.query(Queue).filter_by(id=form_data.queue_id, step=3)
    que = this_queue.first()

    if que:

        if form_data.next_date != 'none':
            this_queue.update({Queue.next_date: form_data.next_date})

        this_queue.update({Queue.step: 4, Queue.upt: True})
       
        db.commit()

        next_que = db.query(Queue).filter_by(room=que.room, step=3, date=now_sanavaqt.strftime("%Y-%m-%d")).order_by(Queue.number.asc()).first()

        if next_que:
            return next_que 
            

        
    else:
        raise HTTPException(status_code=400, detail="Queue topilmadi!")



def complete_diagnosis_finish(id, usr, db):

    this_queue = db.query(Queue).filter_by(id=id, step=4)
    theque = this_queue.first()

    if theque:
        this_queue.update({Queue.step: 5, Queue.completed_at: now_sanavaqt, Queue.upt: True})

        setting = db.query(Setting).first()

        # if setting:
        #     ADDING_HOURS = setting.recall_hour
        # else:
        #     ADDING_HOURS = 3

        new_recall = Recall(
            patient_id=theque.patient_id,
            # plan_date=(now_sanavaqt+timedelta(hours=ADDING_HOURS)),
            user_id=usr.id,
            queue_id = theque.id
        )

        db.add(new_recall)
        db.commit()

        next_queues = db.query(Queue).filter_by(patient_id=theque.patient_id, step=1).options(
            joinedload(Queue.doctor) \
            .subqueryload(Doctor.user) \
                .load_only(
                User.name,
                User.phone,
            ),
            joinedload(Queue.patient).subqueryload("*"),
            joinedload(Queue.service),
        ).all()


        return {
            "next_queues": next_queues,
            "queue": db.query(Queue).options(
            joinedload(Queue.doctor) \
            .subqueryload(Doctor.user) \
                .load_only(
                User.name,
                User.phone,
            ),
            joinedload(Queue.patient).subqueryload("*"),
            joinedload(Queue.service),
            joinedload(Queue.diagnosiss),
            joinedload(Queue.recipes).subqueryload(Recipe.drug),
        ).filter_by(id=id).first()
        } 

    else:
        raise HTTPException(status_code=400, detail="Queue topilmadi!")

def cancel_queue(id, usr, db):

    this_queue = db.query(Queue).filter_by(id=id).filter(Queue.step > 0)



    if this_queue.first():
        if this_queue.first().step < 4:

            this_queue.update({Queue.step: 0, Queue.cancel_user_id: usr.id, Queue.upt: True})
            db.query(Income).filter_by(queue_id=id).delete()

            db.commit()

            return 'success'

    else:
        raise HTTPException(status_code=400, detail="Queue topilmadi!")


