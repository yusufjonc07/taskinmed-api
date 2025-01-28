    
from fastapi import HTTPException
from app.models.state import State


def get_count_states(region_id, usr, db):

    return db.query(State).filter_by(region_id=region_id).count()


def get_all_states(region_id, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(State).filter(State.region_id == region_id).order_by(State.id.desc()).offset(offset).limit(limit).all()


def read_state(id, usr, db):

    this_state = db.query(State).filter(State.id == id).first()

    if this_state:
        return this_state
    else:
        raise HTTPException(status_code=400, detail="State topilmadi!")


def create_state(form_data, usr, db):

    new_state = State(
        name=form_data.name,
        region_id=form_data.region_id,
    )

    db.add(new_state)

    db.commit()
    return new_state.id


def update_state(id, form_data, usr, db):

    this_state = db.query(State).filter(State.id == id)

    if this_state.first():
        this_state.update({
            State.name: form_data.name,
            State.region_id: form_data.region_id,
            State.upt: True
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="State topilmadi!")


def delete_state(id, usr, db):

    this_state = db.query(State).filter(State.id == id)

    if this_state.first():
        this_state.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="State topilmadi!")       
    