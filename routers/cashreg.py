    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.cashreg import *
from models.cashreg import *
from schemas.cashreg import *

cashreg_router = APIRouter(tags=['Cashreg Endpoint'])


@cashreg_router.get("/cashregs", description="This router returns list of the cashregs using pagination")
async def get_cashregs_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_cashregs(page, limit, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@cashreg_router.post("/cashreg/create", description="This router is able to add new cashreg and return cashreg id")
async def create_new_cashreg(
    form_data: NewCashreg,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_cashreg(form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@cashreg_router.put("/cashreg/{id}/update", description="This router is able to update cashreg")
async def update_one_cashreg(
    id: int,
    form_data: NewCashreg,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_cashreg(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    