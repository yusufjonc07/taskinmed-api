    
from fastapi import HTTPException
from app.models.recall import Recall
from sqlalchemy.orm import joinedload
from sqlalchemy import func
import math
from . request import insert_req
from app.models.deleteds import Deleteds
from app.models.doctor import Doctor


def get_count_recalls(usr, db):
    return db.query(Recall).count()


def get_all_recalls(patient_id, from_date, to_date, queue, completed, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    recalls = db.query(Recall).options(
        joinedload(Recall.patient),
        joinedload(Recall.operator),
        joinedload(Recall.queue).subqueryload("*"),
    )

    recalls = recalls.filter_by(status=completed)

    if patient_id > 0:
        recalls = recalls.filter_by(patient_id=patient_id)
    
    if completed:
        recalls = recalls.filter(
            func.date(Recall.plan_date) >= from_date,
            func.date(Recall.plan_date) <= to_date,
        )
    else:
        if queue:
            recalls = recalls.filter(Recall.queue_id > 0)
        else:
            recalls = recalls.filter(Recall.queue_id == 0)

    recalls = recalls.order_by(Recall.plan_date.asc()).offset(offset).limit(limit)

    return {
        "data": recalls.all(),
        "count": math.ceil(recalls.count() / limit),
        "page": page,
        "limit": limit,
    }



def read_recall(id, usr, db):

    this_recall = db.query(Recall).filter(Recall.id == id).first()

    if this_recall:
        return this_recall
    else:
        raise HTTPException(status_code=400, detail="Recall topilmadi!")


def create_recall(form_data, usr, db):

    new_recall = Recall(
        patient_id=form_data.patient_id,
        plan_date=form_data.plan_date,  
        user_id=usr.id,
    )

    db.add(new_recall)

    db.commit()
    return new_recall.id



def talked_recall(id, form_data, usr, db):

    this_recall = db.query(Recall).filter(Recall.id == id)

    if this_recall.first():
        this_recall.update({
            Recall.comment: form_data.comment,
            Recall.talk_type: form_data.talk_type,
            Recall.status: True,
            Recall.upt: True
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Recall topilmadi!")

def update_recall(id, form_data, usr, db):

    this_recall = db.query(Recall).filter(Recall.id == id)

    if this_recall.first():
        this_recall.update({
            Recall.plan_date: form_data.plan_date,
            Recall.upt: True
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Recall topilmadi!")


def delete_recall(id, usr, db):

    this_recall = db.query(Recall).filter(Recall.id == id)

    if this_recall.first():
        this_recall.delete()
       

        db.add(Deleteds(
            table='recall',
            item_id=id
        ))

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Recall topilmadi!")       
    