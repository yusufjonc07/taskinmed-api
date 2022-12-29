    
from fastapi import HTTPException
from models.queue import Queue, now_sanavaqt
from sqlalchemy.orm import joinedload
from models.service import Service
from models.user import User
from models.doctor import Doctor
from models.patient import Patient
from manager import *
from sqlalchemy import or_
import math
from trlatin import tarjima


def get_count_queues(usr, db):

    return db.query(Queue).count()


def get_all_queues(page, limit, usr, db, step, search):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    qs = db.query(Queue).filter_by(step=step) \
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


    data = qs.order_by(Queue.number.asc()).offset(offset).limit(limit)

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
        raise HTTPException(status_code=400, detail="Queue was not found!")


def create_queue(form_data, p_id, usr, db):

    try:
        last_queue = db.query(Queue).filter_by(room=form_data.room, date=form_data.date).order_by(Queue.number.desc()).first()

        if last_queue:
            number = last_queue.number + 1
        else:
            number = 1

        new_queue = Queue(
            room=form_data.room,
            doctor_id=form_data.doctor_id,
            service_id=form_data.service_id,
            number=number,
            date=form_data.date,
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
            Queue.number: form_data.number,
            Queue.completed_at: form_data.completed_at,
            Queue.step: form_data.step,
            Queue.user_id: form_data.user_id,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Queue was not found!")

def confirm_queue(id, db):

    this_queue = db.query(Queue).filter_by(id=id, step=2)

    if this_queue.first():
        this_queue.update({Queue.step: 3})
        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Queue was not found!")

async def confirm_diagnosis(id, db):

    this_queue = db.query(Queue).filter_by(id=id, step=3)
    que = this_queue.first()

    if que:
        this_queue.update({Queue.step: 4})
        db.commit()

        next_que = db.query(Queue).filter_by(room=que.room, step=3, date=now_sanavaqt.strftime("%Y-%m-%d")).order_by(Queue.number.asc()).first()

        if next_que:
            await manager.queue({
                "room": next_que.room,
                "number": next_que.number,
                "patient": next_que.patient.surename + " " + next_que.patient.name,
                "service": next_que.service.name
            })

        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Queue was not found!")



def complete_diagnosis_finish(id, db):

    this_queue = db.query(Queue).filter_by(id=id, step=4)

    if this_queue.first():
        this_queue.update({Queue.step: 5, Queue.completed_at: now_sanavaqt})
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
        raise HTTPException(status_code=400, detail="Queue was not found!")

def cancel_queue(id, usr, db):

    this_queue = db.query(Queue).filter_by(id=id).filter(Queue.step > 0)

    if this_queue.first():
        this_queue.update({Queue.step: 0, Queue.cancel_user_id: usr.id})
        db.commit()

        return 'success'

    else:
        raise HTTPException(status_code=400, detail="Queue was not found!")


    