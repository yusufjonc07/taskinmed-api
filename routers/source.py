    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.source import *
from models.source import *
from schemas.source import *
from typing import List

source_router = APIRouter(tags=['Source Endpoint'])


@source_router.get("/sources", description="This router returns list of the sources using pagination")
async def get_sources_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_sources(page, limit, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@source_router.post("/source/create", description="This router is able to add new source and return source id")
async def create_new_source(
    form_datas: List[NewSource],
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        for form_data in form_datas:
            create_source(form_data, usr, db)

        raise HTTPException(status_code=200, detail="Success!")
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@source_router.put("/source/{id}/update", description="This router is able to update source")
async def update_one_source(
    id: int,
    form_data: NewSource,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_source(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    