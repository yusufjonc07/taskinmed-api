    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.doctor import *
from models.doctor import *
from schemas.doctor import *

doctor_router = APIRouter(tags=['Doctor Endpoint'])


@doctor_router.get("/doctors", description="This router returns list of the doctors using pagination")
async def get_doctors_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_doctors(page, limit, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@doctor_router.post("/doctor/create", description="This router is able to add new doctor and return doctor id")
async def create_new_doctor(
    form_data: NewDoctor,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_doctor(form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@doctor_router.put("/doctor/{id}/update", description="This router is able to update doctor")
async def update_one_doctor(
    id: int,
    form_data: NewDoctor,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_doctor(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    