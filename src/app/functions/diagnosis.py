    
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from app.models.diagnosis import Diagnosis
from app.models.queue import Queue
from app.models.recipe import Recipe
from app.models.user import User
from app.functions.recipe import create_recipe
from app.functions.request import insert_req


def get_count_diagnosiss(patient_id, usr, db):

    return db.query(Diagnosis).filter(Diagnosis.patient_id==patient_id).count()


def get_all_diagnosiss(page, patient_id, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    dgs = db.query(Diagnosis).options(
        joinedload(Diagnosis.patient),
        joinedload(Diagnosis.user).load_only(User.name, User.phone),
        joinedload(Diagnosis.recipes).subqueryload(Recipe.drug),
    )

    if patient_id > 0:
        dgs = dgs.filter_by(patient_id=patient_id)

    if usr.role == 'doctor':
        dgs = dgs.filter_by(user_id=usr.id)
        
    return dgs.order_by(Diagnosis.id.desc()).offset(offset).limit(limit).all()


def read_diagnosis(id, usr, db):

    this_diagnosis = db.query(Diagnosis).filter(Diagnosis.id == id).first()

    if this_diagnosis:
        return this_diagnosis
    else:
        raise HTTPException(status_code=400, detail="Tashxis topilmadi!")


def create_diagnosis(form_data, usr, db):
    
    upt = db.query(Queue).filter_by(id=form_data.queue_id, step=3)
    queue = upt.first()

    if queue:
        
        new_diagnosis = Diagnosis(
            illness=form_data.illness,
            description=form_data.description,
            user_id=usr.id,
            queue_id=queue.id,
            patient_id=queue.patient_id,
        )

        db.add(new_diagnosis)
        db.flush()

        db.query(Queue).filter_by(id=form_data.queue_id).update({
            Queue.complaint: form_data.description
        })

        for one_recipe in form_data.recipes:
            create_recipe(one_recipe, new_diagnosis.id, queue,  usr, db)

        db.commit()

        return 'success'
    else:
        raise HTTPException(status_code=400, detail="Navbat topilmadi!")
    


def update_diagnosis(id, form_data, usr, db):

    this_diagnosis = db.query(Diagnosis).filter(Diagnosis.id == id)

    if this_diagnosis.first():
        this_diagnosis.update({
            Diagnosis.illness: form_data.illness,
            Diagnosis.description: form_data.description,
            Diagnosis.upt: True,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Tashxis topilmadi!")


def delete_diagnosis(id, usr, db):

    this_diagnosis = db.query(Diagnosis).filter(Diagnosis.id == id)

    if this_diagnosis.first():
        this_diagnosis.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Tashxis topilmadi!")       
    