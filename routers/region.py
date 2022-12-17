from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.region import *
from models.region import *
from schemas.region import *

region_router = APIRouter(tags=['Region Endpoint'])


@region_router.get("/regions", description="This router returns list of the regions using pagination")
async def get_regions_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_regions(page, limit, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@region_router.post("/region/create", description="This router is able to add new region and return region id")
async def create_new_region(
    form_data: NewRegion,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_region(form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@region_router.put("/region/{id}/update", description="This router is able to update region")
async def update_one_region(
    id: int,
    form_data: NewRegion,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_region(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    