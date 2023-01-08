    
from fastapi import HTTPException
from models.queue import Queue, now_sanavaqt
from sqlalchemy.orm import joinedload
from models.service import Service
from models.user import User
from models.doctor import Doctor
from models.setting import Setting
from models.income import Income
from models.recall import Recall
from models.patient import Patient, now_sanavaqt
from manager import *
from sqlalchemy import or_
import math
from trlatin import tarjima
from datetime import timedelta
from .request import insert_req


def get_count_queues(usr, db):

    return db.query(Queue).count()


def get_all_queues(page, limit, usr, db, step, search, patient_id):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    qs = db.query(Queue) \
        .join(Queue.service, aliased=True) \
        .join(Queue.patient, aliased=True) \
        .join(Queue.doctor, aliased=True) \
        .join(Doctor.user, aliased=True) \
        .options(
            joinedload('doctor').subqueryload('user').load_only(
                User.name,
                User.phone,
            ),
            joinedload('patient'),
            joinedload('service'),
            joinedload('diagnosiss') \
            .subqueryload('recipes') \
            .subqueryload('drug'),
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
        qs = qs.filter(Queue.step==step, Queue.date == now_sanavaqt.strftime("%Y-%m-%d")).order_by(Queue.number.asc())

    data = qs.offset(offset).limit(limit)

    return {
        "data": data.all(),
        "count": math.ceil(data.count() / limit),
        "page": page,
        "limit": limit,
    }

def read_queue(id, usr, db):

    this_queue = db.query(Queue) \
        .join(Queue.service, aliased=True) \
        .join(Queue.patient, aliased=True) \
        .join(Queue.doctor, aliased=True) \
        .join(Doctor.user, aliased=True) \
        .options(
            joinedload('doctor').subqueryload('user').load_only(
                User.name,
                User.phone,
            ),
            joinedload('patient'),
            joinedload('service'),
            joinedload('diagnosiss') \
            .subqueryload('recipes') \
            .subqueryload('drug'),
        ).filter(Queue.id == id).first()

    if this_queue:
        return this_queue
    else:
        raise HTTPException(status_code=400, detail="Queue topilmadi!")


def create_queue(form_data, p_id, usr, db):

    try:
        last_queue = db.query(Queue).filter_by(room=form_data.room, date=now_sanavaqt.strftime("%Y-%m-%d")).order_by(Queue.number.desc()).first()

        if last_queue:
            number = last_queue.number + 1
        else:
            number = 1

        new_queue = Queue(
            room=form_data.room,
            doctor_id=form_data.doctor_id,
            service_id=form_data.service_id,
            time=form_data.time,
            number=number,
            patient_id=p_id,
            user_id=usr.id
        )

        db.add(new_queue)
        db.commit()
        
        return 'success'
    except Exception as e:
        print(e)

def get_unpaid_queues(db):
    return db.query(Queue).options(
            joinedload('doctor').subqueryload('user').load_only(
                User.name,
                User.phone,
            ),
            joinedload('patient'),
            joinedload('service'),
            joinedload('diagnosiss') \
            .subqueryload('recipes') \
            .subqueryload('drug'),
        ).filter_by(step=1).order_by(Queue.id.desc()).all()

def update_queue(id, form_data, usr, db):

    this_queue = db.query(Queue).filter(Queue.id == id)

    if this_queue.first():
        this_queue.update({
            Queue.patient_id: form_data.patient_id,
            Queue.service_id: form_data.service_id,
            Queue.time: form_data.time,
            Queue.number: form_data.number,
            Queue.completed_at: form_data.completed_at,
            Queue.step: form_data.step,
            Queue.user_id: form_data.user_id,
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
        raise HTTPException(status_code=400, detail="Queue topilmadi!")

def confirm_diagnosis(id, db):

    this_queue = db.query(Queue).filter_by(id=id, step=3)
    que = this_queue.first()

    if que:
        this_queue.update({Queue.step: 4, Queue.upt: True,})
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

        if setting:
            ADDING_HOURS = setting.recall_hour
        else:
            ADDING_HOURS = 3

        new_recall = Recall(
            patient_id=theque.patient_id,
            plan_date=(now_sanavaqt+timedelta(hours=ADDING_HOURS)),
            user_id=usr.id,
            queue_id = theque.id
        )

        db.add(new_recall)
        db.commit()


        return db.query(Queue).options(
            joinedload('doctor') \
            .subqueryload('user') \
                .load_only(
                User.name,
                User.phone,
            ),
            joinedload('patient').subqueryload("*"),
            joinedload('service'),
            joinedload('diagnosiss') \
            .subqueryload('recipes') \
            .subqueryload('drug'),
        ).filter_by(id=id).first()

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


    