    
from fastapi import HTTPException
from models.income import Income
from models.patient import Patient
from models.queue import Queue
from models.casher import Casher


def get_count_incomes(usr, db):

    return db.query(Income).count()


def get_all_incomes(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Income).order_by(Income.id.desc()).offset(offset).limit(limit).all()


def read_income(id, usr, db):

    this_income = db.query(Income).filter(Income.id == id).first()

    if this_income:
        return this_income
    else:
        raise HTTPException(status_code=404, detail="Income was not found!")


def create_income(queue_id, usr, db):

    upt = db.query(Queue).filter_by(id=queue_id, step=1)
    queue = upt.first()

    if queue:

        casher = db.query(Casher).filter_by(user_id=usr.id, disabled=False).first()

        if casher:

            new_income = Income(
                value=queue.doctor.cost,
                patient_id=queue.patient_id,
                queue_id=queue.id,
                user_id=usr.id,
                cashreg_id=casher.cashreg_id
            )

            db.add(new_income)
            db.flush()
            
            if new_income.id > 0:
                upt.update({Queue.step: 2})
                db.commit()
                return new_income
            else:
                raise HTTPException(status_code=500, detail="Income was not created!")
        else:
            raise HTTPException(status_code=404, detail="Casher was not found!")
    else:
        raise HTTPException(status_code=404, detail="Queue was not found!")



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
                })

                db.commit()
                return 'Success'
    else:
        raise HTTPException(status_code=404, detail="Income was not found!")


def delete_income(id, usr, db):

    this_income = db.query(Income).filter(Income.id == id)

    if this_income.first():
        this_income.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=404, detail="Income was not found!")       
    