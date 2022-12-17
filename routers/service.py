    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.service import *
from models.service import *
from schemas.service import *
from typing import List

service_router = APIRouter(tags=['Service Endpoint'])


@service_router.get("/services", description="This router returns list of the services using pagination")
async def get_services_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_services(page, limit, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@service_router.post("/service/create", description="This router is able to add new service and return service id")
async def create_new_service(
    form_datas: List[NewService],
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        for form_data in form_datas:
            create_service(form_data, usr, db)
        raise HTTPException(status_code=200, detail="Success!")
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@service_router.put("/service/{id}/update", description="This router is able to update service")
async def update_one_service(
    id: int,
    form_data: NewService,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_service(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    