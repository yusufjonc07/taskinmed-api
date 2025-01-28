    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from app.db import ActiveSession
from sqlalchemy.orm import Session
from app.auth import get_current_active_user
from app.settings import UserSchema
from app.functions.illness_comment import *
from app.models.illness_comment import *
from app.schemas.illness_comment import *

illness_comment_router = APIRouter(tags=['Illness_Comment Endpoint'])


@illness_comment_router.get("/illness_comments", description="This router returns list of the illness_comments using pagination")
async def get_illness_comments_list(
    illness_id:int,
    search: Optional[str] = '',
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return get_all_illness_comments(illness_id, search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@illness_comment_router.post("/illness_comment/create", description="This router is able to add new illness_comment and return illness_comment id")
async def create_new_illness_comment(
    form_data: NewIllness_Comment,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_illness_comment(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@illness_comment_router.put("/illness_comment/{id}/update", description="This router is able to update illness_comment")
async def update_one_illness_comment(
    id: int,
    form_data: NewIllness_Comment,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_illness_comment(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    