    
from fastapi import HTTPException
from models.doctor import Doctor
from sqlalchemy.orm import subqueryload
from models.user import User



def get_count_doctors(user_id, usr, db):

    return db.query(Doctor).filter_by(user_id=user_id).count()


def get_all_doctors(user_id, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Doctor).options(
        subqueryload('user').load_only(
            User.name,
            User.disabled,
            User.phone,
        )
    ).filter_by(user_id=user_id).order_by(Doctor.id.desc()).offset(offset).limit(limit).all()


def read_doctor(id, usr, db):

    this_doctor = db.query(Doctor).filter(Doctor.id == id).first()

    if this_doctor:
        return this_doctor
    else:
        raise HTTPException(status_code=404, detail="Doctor was not found!")


def create_doctor(form_data, usr, db):

    if form_data.cost < 0:
        raise HTTPException(status_code=422, detail="Cost of doctor must be higher than 0!")

    new_doctor = Doctor(
        service_id=form_data.service_id,
        cost=form_data.cost,
        room=form_data.room,
        user_id=form_data.user_id,
    )

    db.add(new_doctor)
    db.commit()

    return new_doctor.id


def update_doctor(id, form_data, usr, db):

    this_doctor = db.query(Doctor).filter(Doctor.id == id)

    if this_doctor.first():
        
        this_doctor.update({
            Doctor.service_id: form_data.service_id,
            Doctor.room_id: form_data.room_id,
            Doctor.user_id: form_data.user_id,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Doctor was not found!")


def delete_doctor(id, usr, db):

    this_doctor = db.query(Doctor).filter(Doctor.id == id)

    if this_doctor.first():
        this_doctor.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=404, detail="Doctor was not found!")       
    