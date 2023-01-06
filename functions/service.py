    
from fastapi import HTTPException
from models.service import Service


def get_count_services(usr, db):

    return db.query(Service).count()


def get_all_services(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Service).order_by(Service.id.desc()).offset(offset).limit(limit).all()


def read_service(id, usr, db):

    this_service = db.query(Service).filter(Service.id == id).first()

    if this_service:
        return this_service
    else:
        raise HTTPException(status_code=400, detail="Service was not found!")


def create_service(req, form_data, usr, db):

    new_service = Service(
        name=form_data.name,
        disabled=form_data.disabled,
        user_id=usr.id,
    )

    db.add(new_service)

    db.commit()
    return new_service.id


def update_service(req, id, form_data, usr, db):

    this_service = db.query(Service).filter(Service.id == id)

    if this_service.first():
        this_service.update({
            Service.name: form_data.name,
            Service.disabled: form_data.disabled,
            Service.user_id: usr.id,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Service was not found!")


def delete_service(id, usr, db):

    this_service = db.query(Service).filter(Service.id == id)

    if this_service.first():
        this_service.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Service was not found!")       
    