from fastapi import HTTPException
from app.models.income import Income
from app.models.patient import Patient
from app.models.queue import Queue
from app.models.casher import Casher
from app.models.doctor import Doctor
from app.models.user import User
from app.trlatin import tarjima
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, func

def get_count_incomes(search, from_date, to_date, usr, db):

    incomes = db.query(Income).join(Income.patient)

    if len(search) > 0:
        incomes = incomes.filter(
            or_(
                Patient.name.like(f"%{tarjima(search, 'uz')}%"),
                Patient.name.like(f"%{tarjima(search, 'ru')}%"),
            )
        )

    return incomes.filter(
            func.date(Income.created_at) >= from_date,
            func.date(Income.created_at) <= to_date,
        ).count()


def get_all_incomes(search, from_date, to_date, page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    incomes = db.query(Income).join(Income.patient)

    if len(search) > 0:
        incomes = incomes.filter(
            or_(
                Patient.name.like(f"%{tarjima(search, 'uz')}%"),
                Patient.name.like(f"%{tarjima(search, 'ru')}%"),
            )
        )

    return incomes.filter(
            func.date(Income.created_at) >= from_date,
            func.date(Income.created_at) <= to_date,
        ).options(joinedload(Income.patient), joinedload(Income.queue).subqueryload(Queue.service)).order_by(Income.created_at.desc()).offset(offset).limit(limit).all()


def read_income(id, usr, db):

    this_income = db.query(Income).filter(Income.id == id).first()

    if this_income:
        return this_income
    else:
        raise HTTPException(status_code=400, detail="Income topilmadi!")


def create_income(form_data, usr, db):

    upt = db.query(Queue).filter_by(id=form_data.queue_id, step=1)
    queue = upt.first()

    if queue:

        casher = db.query(Casher).filter_by(user_id=usr.id, disabled=False).first()

        if casher:

            new_income = Income(
                value=queue.doctor.cost,
                patient_id=queue.patient_id,
                queue_id=queue.id,
                method=form_data.method,
                user_id=usr.id,
                cashreg_id=casher.cashreg_id
            )

            db.add(new_income)
            db.flush()
            
            if new_income.id > 0:
                
                upt.update({Queue.step: 3, Queue.upt: True})
                db.commit()

                return db.query(Queue) \
                    .filter_by(id=form_data.queue_id, step=3) \
                        .options(
                            joinedload(Queue.incomes),
                            joinedload(Queue.patient),
                            joinedload(Queue.service),
                            joinedload(Queue.doctor).subqueryload(Doctor.user).load_only(
                                User.name,
                                User.phone,
                            ),
                        ).first()
            else:
                raise HTTPException(status_code=500, detail="Income was not created!")
        else:
            raise HTTPException(status_code=400, detail="Casher topilmadi!")
    else:
        raise HTTPException(status_code=400, detail="Queue topilmadi!")



def update_income(id, queue_id, usr, db):

    this_income = db.query(Income).filter(Income.id == id)

    if this_income.first():


        upt = db.query(Queue).filter_by(id=queue_id, step=1)
        queue = upt.first()

        if queue:

            casher = db.query(Casher).filter_by(user_id=usr.id, disabled=False).first()

            if casher:
                this_income.update({
                    Income.value: queue.doctor.cost,
                    Income.patient_id: queue.patient_id,
                    Income.queue_id: queue.id,
                    Income.user_id: usr.id,
                    Income.cashreg_id: casher.cashreg_id,
                    Income.upt: True,
                })

                db.commit()
                return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Income topilmadi!")


def delete_income(id, usr, db):

    this_income = db.query(Income).filter(Income.id == id)

    if this_income.first():
        this_income.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Income topilmadi!")       
    