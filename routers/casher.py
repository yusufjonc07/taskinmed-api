    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.casher import *
from models.casher import *
from schemas.casher import *

casher_router = APIRouter(tags=['Casher Endpoint'])


@casher_router.get("/cashers", description="This router returns list of the cashers using pagination")
async def get_cashers_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_cashers(page, limit, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")



@casher_router.post("/casher/create", description="This router is able to add new casher and return casher id")
async def create_new_casher(
    form_data: NewCasher,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_casher(form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@casher_router.put("/casher/{id}/update", description="This router is able to update casher")
async def update_one_casher(
    id: int,
    form_data: NewCasher,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_casher(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    