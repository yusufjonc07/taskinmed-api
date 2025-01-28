    
from fastapi import HTTPException
from app.models.illness import Illness
from sqlalchemy import or_
import math
from app.trlatin import tarjima




def get_all_illnesss(service_id, search, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    qs = db.query(Illness).filter_by(service_id=service_id)
       

    if len(search) > 0:
        qs = qs.filter(
            or_(
                Illness.name.like(f"%{tarjima(search, 'uz')}%"),
                Illness.name.like(f"%{tarjima(search, 'ru')}%"),
            )       
        )

    data = qs.offset(offset).limit(limit)

    return {
        "data": data.all(),
        "count": math.ceil(qs.count() / limit),
        "page": page,
        "limit": limit,
    }


def read_illness(id, usr, db):

    this_illness = db.query(Illness).filter(Illness.id == id).first()

    if this_illness:
        return this_illness
    else:
        raise HTTPException(status_code=400, detail="Illness was not found!")


def create_illness(form_data, usr, db):

    new_illness = Illness(
        name=form_data.name,
        service_id=form_data.service_id,
        user_id=usr.id,
    )

    db.add(new_illness)

    db.commit()
    return new_illness.id


def update_illness(id, form_data, usr, db):

    this_illness = db.query(Illness).filter(Illness.id == id)

    if this_illness.first():
        this_illness.update({
            Illness.name: form_data.name,
            Illness.service_id: form_data.service_id
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Illness was not found!")


def delete_illness(id, usr, db):

    this_illness = db.query(Illness).filter(Illness.id == id)

    if this_illness.first():
        this_illness.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Illness was not found!")       
    