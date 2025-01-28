    
from fastapi import HTTPException
from app.models.illness_comment import Illness_Comment
from sqlalchemy import or_
import math
from app.trlatin import tarjima
from sqlalchemy.orm import joinedload

def get_count_illness_comments(usr, db):

    return db.query(Illness_Comment).count()


def get_all_illness_comments(illness_id, search, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    qs = db.query(Illness_Comment).options(
        joinedload(Illness_Comment.service)
    ).filter_by(illness_id=illness_id)
       

    if len(search) > 0:
        qs = qs.filter(
            or_(
                Illness_Comment.comment.like(f"%{tarjima(search, 'uz')}%"),
                Illness_Comment.comment.like(f"%{tarjima(search, 'ru')}%"),
            )       
        )

    data = qs.offset(offset).limit(limit)

    return {
        "data": data.all(),
        "count": math.ceil(qs.count() / limit),
        "page": page,
        "limit": limit,
    }


def read_illness_comment(id, usr, db):

    this_illness_comment = db.query(Illness_Comment).filter(Illness_Comment.id == id).first()

    if this_illness_comment:
        return this_illness_comment
    else:
        raise HTTPException(status_code=400, detail="Illness_Comment was not found!")


def create_illness_comment(form_data, usr, db):

    new_illness_comment = Illness_Comment(
        service_id=form_data.service_id,
        comment=form_data.comment,
    )

    db.add(new_illness_comment)

    db.commit()
    return new_illness_comment.id


def update_illness_comment(id, form_data, usr, db):

    this_illness_comment = db.query(Illness_Comment).filter(Illness_Comment.id == id)

    if this_illness_comment.first():
        this_illness_comment.update({
            Illness_Comment.service_id: form_data.service_id,
            Illness_Comment.comment: form_data.comment,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Illness_Comment was not found!")


def delete_illness_comment(id, usr, db):

    this_illness_comment = db.query(Illness_Comment).filter(Illness_Comment.id == id)

    if this_illness_comment.first():
        this_illness_comment.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Illness_Comment was not found!")       
    