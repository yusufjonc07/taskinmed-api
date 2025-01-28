from fastapi import HTTPException
from app.models.state import State
from app.models.source import Source
from sqlalchemy import func
from app.models.queue import Queue
from app.models.service import Service
from app.models.patient import Patient
from app.models.partner import Partner
from app.models.partner_employee import Partner_Employee
from app.models.user import User
from app.models.doctor import Doctor
from app.models.recipe import Recipe
from app.models.income import Income
from app.models.expence import Expence
from sqlalchemy.orm import joinedload
from app.models.diagnosis import Diagnosis
from json import JSONEncoder


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
        
    serrep_res = []
    for one in serrep.all():
        serrep_res.append({
            "id":one.id,
            "name":one.name,
            "count":one.count,
        })


    patrep = db.query(func.count(Queue.id).label("count"), State.id, State.name).select_from(State) \
        .join(State.patients) \
        .join(Patient.queues) \
        .filter(
            Queue.step > 0,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(State.id)
    
    patrep_res = []
    for one in patrep.all():
        patrep_res.append({
            "id":one.id,
            "name":one.name,
            "count":one.count,
        })
       

    sources = db.query(func.count(Queue.id).label("count"), Source.id, Source.name) \
        .join(Source.patients) \
        .join(Patient.queues) \
        .filter(
            Queue.step > 0,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(Source.id)
    
    sources_res = []
    for one in sources.all():
        sources_res.append({
            "id":one.id,
            "name":one.name,
            "count":one.count,
        })

    partners = db.query(func.count(Queue.id).label("count"), Partner.id, Partner.name) \
        .join(Partner.patients) \
        .join(Patient.queues) \
        .filter(
            Queue.step > 0,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(Partner.id)
    
    partners_res = []
    for one in partners.all():
        partners_res.append({
            "id":one.id,
            "name":one.name,
            "count":one.count,
        })

    partner_employees = db.query(func.count(Queue.id).label("count"), Partner_Employee.id, Partner_Employee.name, Partner.name.label('partner_name')) \
        .join(Partner_Employee.patients) \
        .join(Patient.queues) \
        .filter(
            Queue.step > 0,
            func.date(Queue.created_at) >= from_date,
            func.date(Queue.created_at) <= to_date,
        ) \
        .group_by(Partner_Employee.id)
    
    partner_employees_res = []
    for one in partner_employees.all():
        partner_employees_res.append({
            "id":one.id,
            "name":one.name,
            "count":one.count,
        })

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
    
    doctors_res = []
    for one in doctors.all():
        doctors_res.append({
            "name":one.name,
            "count":one.count,
        })
        

    
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
        'states': patrep_res,
        'services': serrep_res,
        'sources': sources_res,
        'doctors': doctors_res,
        'partners': partners_res,
        'partner_employees': partner_employees_res,
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

