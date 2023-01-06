    
from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.patient import *
from functions.queue import *
from models.patient import *
from schemas.patient import *
from typing import Optional
import math

patient_router = APIRouter(tags=['Patient Endpoint'])


@patient_router.get("/patients", description="This router returns list of the patients using pagination")
async def get_patients_list(
    search: Optional[str] = '',
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_patients(search, page, limit, usr, db),
            "count": math.ceil(get_count_patients(search, usr, db) / limit),
            "page": page,
            "limit": limit,
        }
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@patient_router.post("/patient/create", description="This router is able to add new patient as well as his queue")
async def create_new_patient(
    form_data: NewPatient,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if usr.role in ['operator', 'admin', 'reception']:
        p_id = create_patient(req, form_data, usr, db)
        if p_id:

            for nq in form_data.queue:
                q_id = create_queue(req, nq, p_id, usr, db)

        return 'success'

    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@patient_router.put("/patient/{id}/update", description="This router is able to update patient")
async def update_one_patient(
    id: int,
    form_data: UpdatePatient,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):

    if not usr.role in ['any_role']:
        return update_patient(req, id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    