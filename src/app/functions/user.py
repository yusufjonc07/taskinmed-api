    
from fastapi import HTTPException
from app.models.user import User
from app.auth import get_password_hash
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
import math
from app.models.casher import Casher
from app.models.doctor import Doctor


def get_count_users(usr, db):

    return db.query(User).count()


def get_all_users(search, page, limit, usr, db):    

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    users = db.query(User).options(
        joinedload(User.doctors).subqueryload(Doctor.service),
        joinedload(User.cashers).subqueryload(Casher.cashreg),
    )

    if len(search) > 0:
        users = users.filter(
            or_(
                User.name.like(f"%{search}%"),
                User.phone.like(f"%{search}%")
            )
        )

    return {
        "data": users.order_by(User.id.desc()).offset(offset).limit(limit).all(),
        "count": math.ceil(users.count() / limit),
        "page": page,
        "limit": limit,
    }

def read_user(id, usr, db):

    this_user = db.query(User).filter(User.id == id).first()

    if this_user:
        return this_user
    else:
        raise HTTPException(status_code=400, detail="User topilmadi!")


def create_user(form_data, usr, db):

    new_user = User(
        name=form_data.name,
        role=form_data.role,
        phone=form_data.phone,
        username=form_data.username,
        password_hash=get_password_hash(form_data.password_hash),
        disabled=form_data.disabled,
    )

    db.add(new_user)

    db.commit()
    return new_user.id


def update_user(id, form_data, usr, db):

    this_user = db.query(User).filter(User.id == id)

    if this_user.first():

        if form_data.password_hash:
            newpaswd = get_password_hash(form_data.password_hash)
        else:
            newpaswd = this_user.first().password_hash

        this_user.update({
            User.name: form_data.name,
            User.role: form_data.role,
            User.phone: form_data.phone,
            User.username: form_data.username,
            User.password_hash: newpaswd,
            User.disabled: form_data.disabled,
            User.upt: True
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="User topilmadi!")


def delete_user(id, usr, db):

    this_user = db.query(User).filter(User.id == id)

    if this_user.first():
        this_user.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="User topilmadi!")       
    