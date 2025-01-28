    
from app.utils import *
from app.functions.cashreg import *
from app.models.cashreg import *
from app.models.income import *
from app.schemas.cashreg import *
import math
from app.functions.request import insert_req
from sqlalchemy import func, or_
from typing import Optional, List
from app.trlatin import tarjima
from sqlalchemy.orm import joinedload

cashreg_router = APIRouter(tags=['Cashreg Endpoint'])


@cashreg_router.get("/cashregs", description="This router returns list of the cashregs using pagination")
async def get_cashregs_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        return {
            "data": get_all_cashregs(page, limit, usr, db),
            "count": math.ceil(get_count_cashregs(usr, db) / limit),
            "page": page,
            "limit": limit,
        }

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@cashreg_router.get("/get_one_cashreg")
async def get_cash_and_balance(
    id:int,
    page: int = 1,
    search: Optional[str] = "",
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin']:

        this_cashreg = db.query(Cashreg).filter(Cashreg.id == id).first()


        if this_cashreg:
            balance = db.query(func.sum(Income.value)).filter(Income.cashreg_id == id, Income.taken==False).scalar()
            
            if page == 1 or page < 1:
                offset = 0
            else:
                offset = (page-1) * limit

            incomes = db.query(Income).join(Income.patient)

            if search:
                incomes = incomes.filter(
                    or_(
                        Patient.name.like(f"%{tarjima(search, 'uz')}%"),
                        Patient.name.like(f"%{tarjima(search, 'ru')}%"),
                    )
                )

            incomes_data = incomes.filter(
                    Income.cashreg_id == id, 
                    Income.taken==False
                ).options(joinedload(Income.patient), joinedload(Income.queue).subqueryload(Queue.service)).order_by(Income.created_at.desc())

            if not balance: 
                balance = 0
            return {
                "balance": balance,
                "cashreg": this_cashreg,
                "data": incomes_data.offset(offset).limit(limit).all(),
                "count": math.ceil(incomes_data.count() / limit),
                "page": page,
                "limit": limit,
                
            } 
        else:
            raise HTTPException(status_code=400, detail="Kassa topilmadi!")

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")



@cashreg_router.get("/get_cashregs_money")
async def get_cash_and_balances(
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin']:

        this_cashregs = db.query(Cashreg).all()

        res = []

        for this_cashreg in this_cashregs:
            balance = db.query(func.sum(Income.value)).filter(Income.cashreg_id == this_cashreg.id, Income.taken==False).scalar()

            if not balance: 
                balance = 0
            
            if balance > 0: 
            
                res.append({
                    "balance": balance,
                    "cashreg": this_cashreg,
                })

        return res
      

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")



@cashreg_router.post("/cashreg/create", description="This router is able to add new cashreg and return cashreg id")
async def create_new_cashreg(
    form_data: NewCashreg,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_cashreg(form_data, usr, db)
        if res:
            
            return res

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")



@cashreg_router.post("/income/accept", description="This router is able to add new cashreg and return cashreg id")
async def create_new_income(
    form_data: List[int],
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['admin']:

        for id in form_data:
            this_income = db.query(Income).filter(Income.id == id)

            if this_income.first():

                this_income.update({
                    Income.taken: True,
                    Income.upt: True,
                })

                db.commit()
                return 'Success'
            else:
                raise HTTPException(status_code=400, detail="Income topilmadi!")

        res = create_cashreg(form_data, usr, db)
        if res:
            
            return res

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@cashreg_router.put("/cashreg/{id}/update", description="This router is able to update cashreg")
async def update_one_cashreg(
    id: int,
    form_data: NewCashreg,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_cashreg(id, form_data, usr, db)
        if res:
            
            return res
            
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    