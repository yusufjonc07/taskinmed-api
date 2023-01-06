    
from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.cashreg import *
from models.cashreg import *
from schemas.cashreg import *
import math
from functions.request import insert_req

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
        raise HTTPException(status_code=400, detail="Access denided!")


@cashreg_router.post("/cashreg/create", description="This router is able to add new cashreg and return cashreg id")
async def create_new_cashreg(
    form_data: NewCashreg,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_cashreg(req, form_data, usr, db)
        if res:
            insert_req(usr, 'post', form_data, req, db)
            return res

    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@cashreg_router.put("/cashreg/{id}/update", description="This router is able to update cashreg")
async def update_one_cashreg(
    id: int,
    form_data: NewCashreg,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_cashreg(req, id, form_data, usr, db)
        if res:
            insert_req(usr, 'put', form_data, req, db)
            return res
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    