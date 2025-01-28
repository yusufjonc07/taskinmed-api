    
from fastapi import HTTPException
from app.models.expence import Expence
from app.trlatin import tarjima
from sqlalchemy import or_, func



def get_count_expences(search, from_date, to_date, usr, db):

    expences = db.query(Expence)

    if len(search) > 0:
        expences = expences.filter(
            or_(
                Expence.comment.like(f"%{tarjima(search, 'uz')}%"),
                Expence.comment.like(f"%{tarjima(search, 'ru')}%"),
            )
        )

    return expences.filter(
            func.date(Expence.created_at) >= from_date,
            func.date(Expence.created_at) <= to_date,
        ).count()


def get_all_expences(search, from_date, to_date, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit


    expences = db.query(Expence)

    if len(search) > 0:
        expences = expences.filter(
            or_(
                Expence.comment.like(f"%{tarjima(search, 'uz')}%"),
                Expence.comment.like(f"%{tarjima(search, 'ru')}%"),
            )
        )

    return expences.filter(
            func.date(Expence.created_at) >= from_date,
            func.date(Expence.created_at) <= to_date,
        ).order_by(Expence.created_at.desc()).offset(offset).limit(limit).all()


def read_expence(id, usr, db):


    this_expence = db.query(Expence).filter(Expence.id == id).first()

    if this_expence:
        return this_expence
    else:
        raise HTTPException(status_code=400, detail="Chiqim topilmadi!")


def create_expence(form_data, usr, db):

    new_expence = Expence(
        comment=form_data.comment,
        value=form_data.value,
        user_id=usr.id,
    )

    db.add(new_expence)

    db.commit()
    return new_expence.id


def update_expence(id, form_data, usr, db):

    this_expence = db.query(Expence).filter(Expence.id == id)

    if this_expence.first():
        this_expence.update({
            Expence.comment: form_data.comment,
            Expence.value: form_data.value,
            Expence.upt: True,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Chiqim topilmadi!")


def delete_expence(id, usr, db):

    this_expence = db.query(Expence).filter(Expence.id == id)

    if this_expence.first():
        this_expence.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Chiqim topilmadi!")       
    