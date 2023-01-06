    
from fastapi import HTTPException
from models.recipe import Recipe


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
        raise HTTPException(status_code=400, detail="Recipe was not found!")


def create_recipe(form_data, dg_id, queue, usr, db):

    new_recipe = Recipe(
        drug_id=form_data.drug_id,
        day=form_data.day,
        time=form_data.time,
        meal=form_data.meal,
        method=form_data.method,
        duration=form_data.duration,
        unit=form_data.unit,
        diagnosis_id=dg_id,
        queue_id=queue.id,
        patient_id=queue.patient_id,
        user_id=usr.id,
    )
    

    db.add(new_recipe)

    db.flush()
    return new_recipe.id


def update_recipe(req, id, form_data, usr, db):

    this_recipe = db.query(Recipe).filter(Recipe.id == id)

    if this_recipe.first():
        this_recipe.update({
            Recipe.user_id: form_data.user_id,
            Recipe.day: form_data.day,
            Recipe.time: form_data.time,
            Recipe.drug_id: form_data.drug_id,
            Recipe.patient_id: form_data.patient_id,
            Recipe.queue_id: form_data.queue_id,
            Recipe.diagnosis_id: form_data.diagnosis_id,
            Recipe.meal: form_data.meal,
            Recipe.method: form_data.method,
            Recipe.duration: form_data.duration,
            Recipe.unit: form_data.unit,
        })

        db.commit()
        return 'Success'
    else:
        raise HTTPException(status_code=400, detail="Recipe was not found!")


def delete_recipe(id, usr, db):

    this_recipe = db.query(Recipe).filter(Recipe.id == id)

    if this_recipe.first():
        this_recipe.delete()

        db.commit()
        return 'This item has been deleted!'
    else:
        raise HTTPException(status_code=400, detail="Recipe was not found!")       
    