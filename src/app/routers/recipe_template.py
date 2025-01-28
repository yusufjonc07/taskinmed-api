    
import math
from operator import or_
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException
from fastapi import HTTPException
from app.db import ActiveSession
from sqlalchemy.orm import Session
from app.auth import get_current_active_user
from app.settings import UserSchema
from app.models.recipe_template import *
from app.trlatin import tarjima
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

recipe_template_router = APIRouter(tags=['Recipe Template Endpoint'])

class NewRecipeTemplate(BaseModel):
    illness_id: int
    drug_id: int
    comment: str

@recipe_template_router.get("/recipe_templates", description="This router returns list of the recipe_templates using pagination")
async def get_recipe_templates_list(
    illness_id:int,
    search: Optional[str] = '',
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:


        if page == 1 or page < 1:
            offset = 0
        else:
            offset = (page-1) * limit

        illness = db.query(Illness).filter_by(id=illness_id)

        if not illness:
            raise HTTPException(status_code=400, detail="Tashxis topilmadi")

        recipes = db.query(Recipe_Template).options(
            joinedload(Recipe_Template.drug)
        ).filter_by(illness_id=illness_id)
        

        if search == True and len(search) > 0:
            recipes = recipes.filter(
                or_(
                    Recipe_Template.comment.like(f"%{tarjima(search, 'uz')}%"),
                    Recipe_Template.comment.like(f"%{tarjima(search, 'ru')}%"),
                )       
            )

        data = recipes.offset(offset).limit(limit)

        return {
            "data": data.all(),
            "count": math.ceil(recipes.count() / limit),
            "page": page,
            "limit": limit,
        }
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@recipe_template_router.post("/recipe_template/create", description="This router is able to add new recipe_template and return recipe_template id")
async def create_new_recipe_template(
    form_data: NewRecipeTemplate,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        new = Recipe_Template(
            drug_id=form_data.drug_id,
            illness_id=form_data.illness_id,
            comment=form_data.comment
        )   
        db.add(new)
        db.commit()

        return "success"
    else:
        raise HTTPException(status_code=400, detail="Access denided!")


@recipe_template_router.put("/recipe_template/{id}/update", description="This router is able to update recipe_template")
async def update_one_recipe_template(
    id: int,
    form_data: NewRecipeTemplate,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        recip = db.query(Recipe_Template).filter_by(id=id)
        recipe = recip.first()

        if recipe:

            recip.update({
                Recipe_Template.illness_id:form_data.illness_id,
                Recipe_Template.drug_id:form_data.drug_id,
                Recipe_Template.comment:form_data.comment,
            })

            db.commit()

            return "success"

    else:
        raise HTTPException(status_code=400, detail="Access denided!")       
    