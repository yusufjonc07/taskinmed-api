    
from fastapi import HTTPException
from models.casher import Casher
from sqlalchemy.orm import subqueryload, joinedload
from models.user import User



def get_count_cashers(usr, db):

    return db.query(Casher).count()


def get_all_cashers(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Casher).options(
        joinedload('cashreg'),
        subqueryload('user').load_only(
            User.name,
            User.disabled,
            User.phone,
        ),
        
    ).order_by(Casher.id.desc()).offset(offset).limit(limit).all()


def read_casher(id, usr, db):

    this_casher = db.query(Casher).filter(Casher.id == id).first()

    if this_casher:
        return this_casher
    else:
        raise HTTPException(status_code=404, detail="Casher was not found!")


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
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Casher was not found!")


def delete_casher(id, usr, db):

    this_casher = db.query(Casher).filter(Casher.id == id)

    if this_casher.first():
        this_casher.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=404, detail="Casher was not found!")       
    