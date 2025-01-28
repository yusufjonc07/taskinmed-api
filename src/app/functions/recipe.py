    
from fastapi import HTTPException
from app.models.recipe import Recipe
from app.models.deleteds import Deleteds


def get_count_recipes(usr, db):

    return db.query(Recipe).count()


def get_all_recipes(page, limit, usr, db):

    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    return db.query(Recipe).order_by(Recipe.id.desc()).offset(offset).limit(limit).all()


def read_recipe(id, usr, db):

    this_recipe = db.query(Recipe).filter(Recipe.id == id).first()

    if this_recipe:
        return this_recipe
    else:
        raise HTTPException(status_code=400, detail="Recipe topilmadi!")


def create_recipe(form_data, dg_id, queue, usr, db):

    new_recipe = Recipe(
        comment=form_data.unit,
        drug_id=form_data.drug_id,
        diagnosis_id=dg_id,
        queue_id=queue.id,
        patient_id=queue.patient_id,
        user_id=usr.id,
    )
    
    db.add(new_recipe)

    db.flush()
    return new_recipe.id


def update_recipe(id, form_data, usr, db):

    this_recipe = db.query(Recipe).filter(Recipe.id == id)

    if this_recipe.first():
        this_recipe.update({
            Recipe.user_id: form_data.user_id,
            Recipe.drug_id: form_data.drug_id,
            Recipe.patient_id: form_data.patient_id,
            Recipe.queue_id: form_data.queue_id,
            Recipe.diagnosis_id: form_data.diagnosis_id,
            Recipe.comment: form_data.comment,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Recipe topilmadi!")


def delete_recipe(id, usr, db):

    this_recipe = db.query(Recipe).filter(Recipe.id == id)

    if this_recipe.first():
        this_recipe.delete()
        db.add(Deleteds(
            table='recipe',
            item_id=id
        ))
        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Recipe topilmadi!")       
    