    
from app.utils import *
from app.functions.recipe import *
from app.models.recipe import *
from app.schemas.recipe import *
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
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


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

                
                return "success"    

        raise HTTPException(status_code=400, detail="Diagnosis not found!")
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@recipe_router.put("/recipe/{id}/update", description="This router is able to update recipe")
async def update_one_recipe(
    id: int,
    form_data: NewRecipe,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_recipe(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       


@recipe_router.delete("/recipe_delete/{id}", description="This router is able to delete recipe")
async def delete_one_recipe(
    id: int,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = delete_recipe(id, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    