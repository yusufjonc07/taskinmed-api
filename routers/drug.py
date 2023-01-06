    
from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.drug import *
from models.drug import *
from schemas.drug import *
import math

drug_router = APIRouter(tags=['Drug Endpoint'])


@drug_router.get("/drugs", description="This router returns list of the drugs using pagination")
async def get_drugs_list(
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = '',
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_drugs(search, page, limit, usr, db),
            "count": math.ceil(get_count_drugs(search, usr, db) / limit),
            "page": page,
            "limit": limit,
        }

    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@drug_router.post("/drug/create", description="This router is able to add new drug and return drug id")
async def create_new_drug(
    form_data: NewDrug,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_drug(req, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@drug_router.put("/drug/{id}/update", description="This router is able to update drug")
async def update_one_drug(
    id: int,
    form_data: NewDrug,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_drug(req, id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    