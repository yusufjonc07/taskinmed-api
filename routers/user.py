    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.user import *
from models.user import *
from schemas.user import *
import math

user_router = APIRouter(tags=['User Endpoint'])


@user_router.get("/users", description="This router returns list of the users using pagination")
async def get_users_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        return {
            "data": get_all_users(page, limit, usr, db),
            "count": math.ceil(get_count_users(usr, db) / limit),
            "page": page,
            "limit": limit,
        }
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@user_router.post("/user/create", description="This router is able to add new user and return user id")
async def create_new_user(
    form_data: NewUser,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return create_user(form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")


@user_router.put("/user/{id}/update", description="This router is able to update user")
async def update_one_user(
    id: int,
    form_data: NewUser,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_user(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=403, detail="Access denided!")       
    