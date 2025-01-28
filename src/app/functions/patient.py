    
from fastapi import HTTPException
from app.models.patient import Patient
from app.models.user import User
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy import or_
from . request import insert_req

def get_count_patients(search, usr, db):

    pats = db.query(Patient)
    
    if len(search) > 0:
        pats = pats.filter(
            or_(
                Patient.name.like(f"%{search}%"),
                Patient.phone.like(f"%{search}%"),
            )
        )
    return pats.count()


def get_all_patients(search, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit


    pats = db.query(Patient)
    
    if len(search) > 0:
        pats = pats.filter(
            or_(
                Patient.name.like(f"%{search}%"),
                Patient.phone.like(f"%{search}%"),
            )
        )

    return pats.options(
        joinedload(Patient.state),
        joinedload(Patient.region),
        joinedload(Patient.source),
        joinedload(Patient.partner),
        joinedload(Patient.partner_employee),
        joinedload(Patient.user).load_only(
            User.name,
            User.phone,
        ),
    ).order_by(Patient.id.desc()).offset(offset).limit(limit).all()


def read_patient(id, usr, db):

    this_patient = db.query(Patient).filter(Patient.id == id).first()

    if this_patient:
        return this_patient
    else:
        raise HTTPException(status_code=400, detail="Patient topilmadi!")


def create_patient(form_data, usr, db):

    new_patient = Patient(
        name=form_data.name,
        surename=form_data.surename,
        fathername=form_data.fathername,
        age=form_data.age,
        address=form_data.address,
        state_id=form_data.state_id,
        region_id=form_data.region_id,
        source_id=form_data.source_id,
        phone=form_data.phone,
        user_id=usr.id,
        partner_id=form_data.partner_id,
        partner_employee_id=form_data.partner_employee_id,
    )

    db.add(new_patient)
    db.flush()


    return new_patient.id


def update_patient(id, form_data, usr, db):

    this_patient = db.query(Patient).filter(Patient.id == id)

    if this_patient.first():
        this_patient.update({
            Patient.name: form_data.name,
            Patient.surename: form_data.surename,
            Patient.fathername: form_data.fathername,
            Patient.age: form_data.age,
            Patient.address: form_data.address,
            Patient.state_id: form_data.state_id,
            Patient.region_id: form_data.region_id,
            Patient.source_id: form_data.source_id,
            Patient.phone: form_data.phone,
            Patient.partner_id: form_data.partner_id,
            Patient.partner_employee_id: form_data.partner_employee_id,
            Patient.user_id: usr.id,
            Patient.upt: True,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Patient topilmadi!")


def delete_patient(id, usr, db):

    this_patient = db.query(Patient).filter(Patient.id == id)

    if this_patient.first():
        this_patient.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Patient topilmadi!")       
    