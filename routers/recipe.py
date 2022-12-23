    
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from db import ActiveSession
from sqlalchemy.orm import Session
from auth import get_current_active_user
from settings import UserSchema
from functions.recipe import *
from models.recipe import *
from schemas.recipe import *
from typing import List
import math

recipe_router = APIRouter(tags=['Recipe Endpoint'])


@recipe_router.get("/recipes", description="This router returns list of the recipes using pagination")
async def get_recipes_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_recipes(page, limit, usr, db),
            "count": math.ceil(get_count_recipes(usr, db) / limit),
            "page": page,
            "limit": limit,
        }
        return get_all_recipes(page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@recipe_router.post("/recipe/create", description="This router is able to add new recipe and return recipe id")
async def create_new_recipe(
    diagnosis_id: int,
    form_datas: List[NewRecipe],
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        if diagnosis_id > 0:
            diagnosis = db.query(Diagnosis).filter_by(id=diagnosis_id).first()

            if diagnosis:

                for form_data in form_datas:
                    recipe = create_recipe(form_data, diagnosis.id, diagnosis.queue, usr, db)
                db.commit()    

        raise HTTPException(status_code=400, detail="Diagnosis not found!")
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@recipe_router.put("/recipe/{id}/update", description="This router is able to update recipe")
async def update_one_recipe(
    id: int,
    form_data: NewRecipe,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return update_recipe(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    