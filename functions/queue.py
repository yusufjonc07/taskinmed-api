    
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
                Service.name.like(f"%{search}%"),
                Patient.name.like(f"%{search}%"),
                Patient.phone.like(f"%{search}%"),
                User.name.like(f"%{search}%"),
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

    this_queue = db.query(Queue).filter(Queue.id == id).first()

    if this_queue:
        return this_queue
    else:
        raise HTTPException(status_code=404, detail="Queue was not found!")


async def create_queue(form_data, p_id, usr, db):

    last_queue = db.query(Queue).filter_by(doctor_id=form_data.doctor_id, date=form_data.date).order_by(Queue.number.desc()).first()

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
    queuses = get_unpaid_queues(db)
    resp_queues = listtostring(queuses)
    
    await manager.sendtocash(resp_queues)
    return new_queue.id

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
        raise HTTPException(status_code=404, detail="Queue was not found!")

def confirm_queue(id, db):

    this_queue = db.query(Queue).filter_by(id=id, step=2)

    if this_queue.first():
        this_queue.update({Queue.step: 3})
        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Queue was not found!")

def confirm_diagnosis(id, db):

    this_queue = db.query(Queue).filter_by(id=id, step=3)

    if this_queue.first():
        this_queue.update({Queue.step: 4})
        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Queue was not found!")

def complete_diagnosis(id, db):

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
            joinedload('patient'),
            joinedload('service'),
            joinedload('diagnosiss') \
            .subqueryload('recipes') \
            .subqueryload('drug'),
        ).filter_by(id=id).first()

    else:
        raise HTTPException(status_code=404, detail="Queue was not found!")

def cancel_queue(id, usr, db):

    this_queue = db.query(Queue).filter_by(id=id).filter(Queue.step > 0)

    if this_queue.first():
        this_queue.update({Queue.step: 0, Queue.cancel_user_id: usr.id})
        db.commit()

        return 'success'

    else:
        raise HTTPException(status_code=404, detail="Queue was not found!")


    