    
from fastapi import HTTPException
from app.models.drug import Drug
from app.trlatin import tarjima
from sqlalchemy import or_
from . request import insert_req



def get_count_drugs(search, usr, db):

    drugs = db.query(Drug)

    if len(search) > 0:
        drugs = drugs.filter(
            or_(
                Drug.name.like(f"%{tarjima(search, 'uz')}%"),
                Drug.name.like(f"%{tarjima(search, 'ru')}%"),
            )
        )

    return drugs.count()


def get_all_drugs(search, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit


    drugs = db.query(Drug)

    if len(search) > 0:
        drugs = drugs.filter(
            or_(
                Drug.name.like(f"%{tarjima(search, 'uz')}%"),
                Drug.name.like(f"%{tarjima(search, 'ru')}%"),
            )
        )

    return drugs.order_by(Drug.name.asc()).offset(offset).limit(limit).all()


def read_drug(id, usr, db):


    this_drug = db.query(Drug).filter(Drug.id == id).first()

    if this_drug:
        return this_drug
    else:
        raise HTTPException(status_code=400, detail="Dori topilmadi!")


def create_drug(form_data, usr, db):

    new_drug = Drug(
        name=form_data.name,
    )

    db.add(new_drug)

    db.commit()
    
    return new_drug.id


def update_drug(id, form_data, usr, db):

    this_drug = db.query(Drug).filter(Drug.id == id)

    if this_drug.first():
        this_drug.update({
            Drug.name: form_data.name,
            Drug.upt: True,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Dori topilmadi!")


def delete_drug(id, usr, db):

    this_drug = db.query(Drug).filter(Drug.id == id)

    if this_drug.first():
        this_drug.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Dori topilmadi!")       
    