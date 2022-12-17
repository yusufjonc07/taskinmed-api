    
from fastapi import HTTPException
from models.patient import Patient


def get_count_patients(usr, db):

    return db.query(Patient).count()


def get_all_patients(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Patient).order_by(Patient.id.desc()).offset(offset).limit(limit).all()


def read_patient(id, usr, db):

    this_patient = db.query(Patient).filter(Patient.id == id).first()

    if this_patient:
        return this_patient
    else:
        raise HTTPException(status_code=404, detail="Patient was not found!")


def create_patient(form_data, usr, db):

    new_patient = Patient(
        name=form_data.name,
        age=form_data.age,
        address=form_data.address,
        state_id=form_data.state_id,
        region_id=form_data.region_id,
        source_id=form_data.source_id,
        phone=form_data.phone,
        user_id=usr.id,
    )

    db.add(new_patient)
    db.flush()

    return new_patient.id


def update_patient(id, form_data, usr, db):

    this_patient = db.query(Patient).filter(Patient.id == id)

    if this_patient.first():
        this_patient.update({
            Patient.name: form_data.name,
            Patient.age: form_data.age,
            Patient.address: form_data.address,
            Patient.state_id: form_data.state_id,
            Patient.region_id: form_data.region_id,
            Patient.source_id: form_data.source_id,
            Patient.phone: form_data.phone,
            Patient.user_id: usr.id,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Patient was not found!")


def delete_patient(id, usr, db):

    this_patient = db.query(Patient).filter(Patient.id == id)

    if this_patient.first():
        this_patient.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=404, detail="Patient was not found!")       
    