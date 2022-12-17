    
from fastapi import HTTPException
from models.queue import Queue
from sqlalchemy.orm import joinedload
from models.doctor import User
from manager import *


def get_count_queues(usr, db):

    return db.query(Queue).count()


def get_all_queues(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Queue).order_by(Queue.id.desc()).offset(offset).limit(limit).all()


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
            joinedload('service')
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


def delete_queue(id, usr, db):

    this_queue = db.query(Queue).filter(Queue.id == id)

    if this_queue.first():
        this_queue.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=404, detail="Queue was not found!")       
    