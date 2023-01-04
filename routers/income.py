    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.income import *
from models.income import *
import math
from typing import Optional

income_router = APIRouter(tags=['Income Endpoint'])


@income_router.get("/incomes", description="This router returns list of the incomes using pagination")
async def get_incomes_list(
    from_date: Optional[str] = now_sanavaqt.strftime("%Y-%m-01"),
    to_date: str = now_sanavaqt.strftime("%Y-%m-%d"),
    page: int = 1,
    search: Optional[str] = '',
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_incomes(search, from_date, to_date, page, limit, usr, db),
            "count": math.ceil(get_count_incomes(search, from_date, to_date, usr, db) / limit),
            "page": page,
            "limit": limit,
        }
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@income_router.put("/income/{id}/update", description="This router is able to update income")
async def update_one_income(
    id: int,
    queue_id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_income(id, queue_id, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    