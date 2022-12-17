    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.diagnosis import *
from models.diagnosis import *
from schemas.diagnosis import *

diagnosis_router = APIRouter(tags=['Diagnosis Endpoint'])


@diagnosis_router.get("/diagnosiss", description="This router returns list of the diagnosiss using pagination")
async def get_diagnosiss_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_diagnosiss(page, limit, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@diagnosis_router.post("/diagnosis/create", description="This router is able to add new diagnosis and return diagnosis id")
async def create_new_diagnosis(
    form_data: NewDiagnosis,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_diagnosis(form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@diagnosis_router.put("/diagnosis/{id}/update", description="This router is able to update diagnosis")
async def update_one_diagnosis(
    id: int,
    form_data: NewDiagnosis,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_diagnosis(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    