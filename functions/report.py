from fastapi import HTTPException
from models.state import State
from models.source import Source
from sqlalchemy import func
from models.queue import Queue
from models.service import Service
from models.patient import Patient
from models.partner import Partner
from models.partner_employee import Partner_Employee
from models.user import User
from models.doctor import Doctor
from models.recipe import Recipe
from models.income import Income
from models.expence import Expence
from sqlalchemy.orm import joinedload
from models.diagnosis import Diagnosis


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

    serrep = db.query(func.count(Queue.id).label("count"), Service.name, Service.id).select_from(Service) \
        .join(Service.queues) \
        .filter(
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(Service.id)
        

    # patients by states

    patrep = db.query(func.count(Queue.id).label("count"), State.id, State.name) \
        .join(State.patients) \
        .join(Patient.queues) \
        .filter(
            Queue.step > 0,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(State.id)
        

    sources = db.query(func.count(Queue.id).label("count"), Source.id, Source.name) \
        .join(Source.patients) \
        .join(Patient.queues) \
        .filter(
            Queue.step > 0,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(Source.id)

    partners = db.query(func.count(Queue.id).label("count"), Partner.id, Partner.name) \
        .join(Partner.patients) \
        .join(Patient.queues) \
        .filter(
            Queue.step > 0,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(Partner.id)

    partner_employees = db.query(func.count(Queue.id).label("count"), Partner_Employee.id, Partner_Employee.name, Partner.name.label('partner_name')) \
        .join(Partner_Employee.patients) \
        .join(Patient.queues) \
        .filter(
            Queue.step > 0,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(Partner_Employee.id)

    doctors = db.query(func.sum(Income.value).label("summa"), User.name) \
        .join(Income.queue) \
        .join(Queue.doctor) \
        .join(Doctor.user) \
        .filter(
            Income.value > 0,
            func.date(Income.created_at) >= from_date,
            func.date(Income.created_at) <= to_date,
        ) \
        .group_by(User.id)
        

    
    income = db.query(func.sum(Income.value)) .filter(
        func.date(Income.created_at) >= from_date,
        func.date(Income.created_at) <= to_date,
    ) \
    .scalar()

    expence = db.query(func.sum(Expence.value)) .filter(
        func.date(Expence.created_at) >= from_date,
        func.date(Expence.created_at) <= to_date,
    ) \
    .scalar()



    return {
        'states': patrep.all(),
        'services': serrep.all(),
        'sources': sources.all(),
        'doctors': doctors.all(),
        'partners': partners.all(),
        'partner_employees': partner_employees.all(),
        'income': income,
        'expence': expence,
    }


def get_states_report(st_id, from_date, to_date, page, limit,  usr, db):

    # servises
    queues = db.query(Queue) \
        .join(Queue.service) \
        .join(Queue.patient) \
        .join(Queue.doctor) \
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
            joinedload(Queue.doctor).subqueryload(Doctor.user).load_only(
                User.name,
                User.phone,
            ),
            joinedload(Queue.patient),
            joinedload(Queue.service),
            joinedload(Queue.diagnosiss) \
            .subqueryload(Diagnosis.recipes) \
            .subqueryload(Recipe.drug),
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

