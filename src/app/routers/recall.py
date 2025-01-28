from fastapi import Depends, APIRouter, HTTPException, Request
from app.db import ActiveSession
from sqlalchemy.orm import Session
from app.auth import get_current_active_user
from app.settings import UserSchema
from app.functions.recall import *
from app.models.recall import *
from app.schemas.recall import *

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
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@recall_router.post("/recall/create", description="This router is able to add new recall and return recall id")
async def create_new_recall(
    form_data: NewRecall,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_recall(form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@recall_router.put("/recall/{id}/talked", description="This router is able to finish recall")
async def talked_one_recall(
    id: int,
    form_data: TalkedRecall,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = talked_recall(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       


@recall_router.put("/recall/{id}/update", description="This router is able to update recall")
async def update_one_recall(
    id: int,
    form_data: UpdateRecall,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_recall(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       

@recall_router.delete("/recall/{id}/delete", description="This router is able to update recall")
async def delete_one_recall(
    id: int,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = delete_recall(id, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@recall_router.get("/count_of_calls")
async def get_count_of_calls(
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    calls = db.query(Recall).filter_by(status=False)

    return {
        "recall": calls.filter(Recall.queue_id > 0).count(),
        "planning": calls.filter(Recall.queue_id == 0).count()
    }
    