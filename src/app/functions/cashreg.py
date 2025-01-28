from fastapi import HTTPException
from app.models.cashreg import Cashreg


def get_count_cashregs(usr, db):

    return db.query(Cashreg).count()


def get_all_cashregs(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    return db.query(Cashreg).order_by(Cashreg.id.desc()).offset(offset).limit(limit).all()


def read_cashreg(id, usr, db):

    this_cashreg = db.query(Cashreg).filter(Cashreg.id == id).first()

    if this_cashreg:
        return this_cashreg
    else:
        raise HTTPException(status_code=400, detail="Kassa topilmadi!")


def create_cashreg(form_data, usr, db):

    new_cashreg = Cashreg(
        name=form_data.name,
    )

    db.add(new_cashreg)

    db.commit()
    return new_cashreg.id


def update_cashreg(id, form_data, usr, db):

    this_cashreg = db.query(Cashreg).filter(Cashreg.id == id)

    if this_cashreg.first():
        this_cashreg.update({
            Cashreg.name: form_data.name,
            Cashreg.upt: True,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Kassa topilmadi!")


def delete_cashreg(id, usr, db):

    this_cashreg = db.query(Cashreg).filter(Cashreg.id == id)

    if this_cashreg.first():
        this_cashreg.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Kassa topilmadi!")       
    