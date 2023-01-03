    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.recall import *
from models.recall import *
from schemas.recall import *

recall_router = APIRouter(tags=['Recall Endpoint'])


@recall_router.get("/recalls", description="This router returns list of the recalls using pagination")
async def get_recalls_list(
    queue: bool,
    completed: bool,
    page: int = 1,
    limit: int = 10,
    patient_id: Optional[int] = 0,
    from_date: Optional[str] = now_sanavaqt.strftime("%Y-%m-01"),
    to_date: Optional[str] = now_sanavaqt.strftime("%Y-%m-%d"),
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_recalls(patient_id, from_date, to_date, queue, completed, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@recall_router.post("/recall/create", description="This router is able to add new recall and return recall id")
async def create_new_recall(
    form_data: NewRecall,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_recall(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@recall_router.put("/recall/{id}/talked", description="This router is able to finish recall")
async def talked_one_recall(
    id: int,
    form_data: TalkedRecall,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return talked_recall(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       


@recall_router.put("/recall/{id}/update", description="This router is able to update recall")
async def update_one_recall(
    id: int,
    form_data: UpdateRecall,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_recall(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       

@recall_router.delete("/recall/{id}/delete", description="This router is able to update recall")
async def delete_one_recall(
    id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return delete_recall(id, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    