    
from fastapi import HTTPException
from models.diagnosis import Diagnosis


def get_count_diagnosiss(usr, db):

    return db.query(Diagnosis).count()


def get_all_diagnosiss(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Diagnosis).order_by(Diagnosis.id.desc()).offset(offset).limit(limit).all()


def read_diagnosis(id, usr, db):

    this_diagnosis = db.query(Diagnosis).filter(Diagnosis.id == id).first()

    if this_diagnosis:
        return this_diagnosis
    else:
        raise HTTPException(status_code=404, detail="Diagnosis was not found!")


def create_diagnosis(form_data, usr, db):

    new_diagnosis = Diagnosis(
        illness=form_data.illness,
        description=form_data.description,
        user_id=form_data.user_id,
        queue_id=form_data.queue_id,
    )

    db.add(new_diagnosis)

    db.commit()
    return new_diagnosis.id


def update_diagnosis(id, form_data, usr, db):

    this_diagnosis = db.query(Diagnosis).filter(Diagnosis.id == id)

    if this_diagnosis.first():
        this_diagnosis.update({
            Diagnosis.illness: form_data.illness,
            Diagnosis.description: form_data.description,
            Diagnosis.user_id: form_data.user_id,
            Diagnosis.queue_id: form_data.queue_id,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Diagnosis was not found!")


def delete_diagnosis(id, usr, db):

    this_diagnosis = db.query(Diagnosis).filter(Diagnosis.id == id)

    if this_diagnosis.first():
        this_diagnosis.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=404, detail="Diagnosis was not found!")       
    