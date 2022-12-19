from fastapi import HTTPException
from models.state import State
from sqlalchemy import func
from models.queue import Queue
from models.service import Service
from models.patient import Patient
from models.user import User
from models.income import Income
from sqlalchemy.orm import joinedload


def get_patentsrep_count(from_date, to_date, st_id, usr, db):
    return db.query(func.count(Queue.id)) \
        .join(Queue.patient) \
        .filter(
            Patient.state_id == st_id,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .scalar()


def get_servicesrep_count(from_date, to_date, srv_id, usr, db):
    return db.query(func.count(Queue.id)) \
        .filter(
            Queue.service_id == srv_id,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .scalar()

def get_report_index(from_date, to_date, usr, db):

    # servises

    serrep = db.query(func.count(Queue.id).label("count"), Service.name, Service.id) \
        .join(Service.queues) \
        .filter(
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .all()

    # patients by states

    patrep = db.query(func.count(Queue.id).label("count"), State.id, State.name) \
        .join(State.patients) \
        .join(Patient.queues) \
        .filter(
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .all()

    
    income = db.query(func.sum(Income.value)) .filter(
        func.date(Income.created_at) >= from_date,
        func.date(Income.created_at) <= to_date,
    ) \
    .scalar()



    return {
        'states': patrep,
        'services': serrep,
        'income': income,
    }


def get_states_report(st_id, from_date, to_date, page, limit,  usr, db):

    # servises

    queues = db.query(Queue) \
        .join(Queue.service) \
        .join(Queue.patient) \
        .join(Queue.doctor) \
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
        ).filter(
            Patient.state_id == st_id,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        )

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return queues.order_by(Queue.id.desc()).offset(offset).limit(limit).all()

def get_services_report(srv_id, from_date, to_date, page, limit,  usr, db):

    # servises

    queues = db.query(Queue) \
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
        ).filter(
            Queue.service_id == srv_id,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        )

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return queues.order_by(Queue.id.desc()).offset(offset).limit(limit).all()

