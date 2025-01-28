    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from app.db import ActiveSession
from sqlalchemy.orm import Session
from app.auth import get_current_active_user
from app.settings import UserSchema
from app.functions.illness import *
from app.models.illness import *
from app.schemas.illness import *

illness_router = APIRouter(tags=['Illness Endpoint'])


@illness_router.get("/illnesses", description="This router returns list of the illnesss using pagination")
async def get_illnesss_list(
    service_id:int,
    search: Optional[str] = '',
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_illnesss(service_id, search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@illness_router.post("/illness/create", description="This router is able to add new illness and return illness id")
async def create_new_illness(
    form_data: NewIllness,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_illness(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@illness_router.put("/illness/{id}/update", description="This router is able to update illness")
async def update_one_illness(
    id: int,
    form_data: NewIllness,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_illness(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    