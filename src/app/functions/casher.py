    
from fastapi import HTTPException, Request
from app.models.casher import Casher
from sqlalchemy.orm import subqueryload, joinedload
from app.models.user import User


def get_count_cashers(user_id, usr, db):

    casher = db.query(Casher)

    if user_id > 0:
        casher = casher.filter_by(user_id=user_id)

    return casher.count()


def get_all_cashers(user_id, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit


    casher = db.query(Casher).options(
        joinedload(Casher.cashreg),
        subqueryload(Casher.user).load_only(
            User.name,
            User.disabled,
            User.phone,
        ),
    )

    if user_id > 0:
        casher = casher.filter_by(user_id=user_id)

    return casher.order_by(Casher.id.desc()).offset(offset).limit(limit).all()

def read_casher(id, usr, db):

    this_casher = db.query(Casher).filter(Casher.id == id).first()

    if this_casher:
        return this_casher
    else:
        raise HTTPException(status_code=400, detail="Kassachi topilmadi!")


def create_casher(form_data, usr, db):

    new_casher = Casher(
        user_id=form_data.user_id,
        cashreg_id=form_data.cashreg_id,
        disabled=form_data.disabled,
    )

    db.add(new_casher)
    db.commit()

    return new_casher.id


def update_casher(id, form_data, usr, db):

    this_casher = db.query(Casher).filter(Casher.id == id)

    if this_casher.first():
        this_casher.update({
            Casher.user_id: form_data.user_id,
            Casher.cashreg_id: form_data.cashreg_id,
            Casher.disabled: form_data.disabled,
            Casher.upt: True,
        })

        db.commit()
        
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Kassachi topilmadi!")


def delete_casher(id, usr, db):

    this_casher = db.query(Casher).filter(Casher.id == id)

    if this_casher.first():
        this_casher.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Kassachi topilmadi!")       
    