    
from fastapi import HTTPException
from app.models.source import Source


def get_count_sources(usr, db):

    return db.query(Source).count()


def get_all_sources(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Source).order_by(Source.id.desc()).offset(offset).limit(limit).all()


def read_source(id, usr, db):

    this_source = db.query(Source).filter(Source.id == id).first()

    if this_source:
        return this_source
    else:
        raise HTTPException(status_code=400, detail="Source topilmadi!")


def create_source(form_data, usr, db):

    new_source = Source(
        name=form_data.name,
    )

    db.add(new_source)
    db.commit()
    
    return new_source.id


def update_source(id, form_data, usr, db):

    this_source = db.query(Source).filter(Source.id == id)

    if this_source.first():
        this_source.update({
            Source.name: form_data.name,
            Source.upt: True
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Source topilmadi!")


def delete_source(id, usr, db):

    this_source = db.query(Source).filter(Source.id == id)

    if this_source.first():
        this_source.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Source topilmadi!")       
    