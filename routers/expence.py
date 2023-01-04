from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.expence import *
from models.expence import *
from schemas.expence import *
import math
from typing import Optional

expence_router = APIRouter(tags=['Expence Endpoint'])


@expence_router.get("/expences", description="This router returns list of the expences using pagination")
async def get_expences_list(
    from_date: Optional[str] = now_sanavaqt.strftime("%Y-%m-01"),
    to_date: str = now_sanavaqt.strftime("%Y-%m-%d"),
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = '',
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_expences(search, from_date, to_date, page, limit, usr, db),
            "count": math.ceil(get_count_expences(search, from_date, to_date, usr, db) / limit),
            "page": page,
            "limit": limit,
        }

    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@expence_router.post("/expence/create", description="This router is able to add new expence and return expence id")
async def create_new_expence(
    form_data: NewExpence,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_expence(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@expence_router.put("/expence/{id}/update", description="This router is able to update expence")
async def update_one_expence(
    id: int,
    form_data: NewExpence,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_expence(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    