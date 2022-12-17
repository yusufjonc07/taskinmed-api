    
from fastapi import HTTPException
from models.region import Region
from sqlalchemy.orm import joinedload


def get_count_regions(usr, db):

    return db.query(Region).count()


def get_all_regions(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Region).options(joinedload('states')).order_by(Region.id.desc()).offset(offset).limit(limit).all()


def read_region(id, usr, db):

    this_region = db.query(Region).filter(Region.id == id).first()

    if this_region:
        return this_region
    else:
        raise HTTPException(status_code=404, detail="Region was not found!")


def create_region(form_data, usr, db):

    new_region = Region(
        name=form_data.name,
    )

    db.add(new_region)

    db.commit()
    return new_region.id


def update_region(id, form_data, usr, db):

    this_region = db.query(Region).filter(Region.id == id)

    if this_region.first():
        this_region.update({
            Region.name: form_data.name,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Region was not found!")


def delete_region(id, usr, db):

    this_region = db.query(Region).filter(Region.id == id)

    if this_region.first():
        this_region.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=404, detail="Region was not found!")       
    