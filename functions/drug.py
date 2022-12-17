    
from fastapi import HTTPException
from models.drug import Drug


def get_count_drugs(usr, db):

    return db.query(Drug).count()


def get_all_drugs(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Drug).order_by(Drug.id.desc()).offset(offset).limit(limit).all()


def read_drug(id, usr, db):

    this_drug = db.query(Drug).filter(Drug.id == id).first()

    if this_drug:
        return this_drug
    else:
        raise HTTPException(status_code=404, detail="Drug was not found!")


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
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Drug was not found!")


def delete_drug(id, usr, db):

    this_drug = db.query(Drug).filter(Drug.id == id)

    if this_drug.first():
        this_drug.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=404, detail="Drug was not found!")       
    