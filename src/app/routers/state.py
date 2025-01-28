    
from app.utils import *
from app.functions.state import *
from app.schemas.state import *
from app.models.state import *
from typing import List
import math

state_router = APIRouter(tags=['State Endpoint'])


@state_router.get("/states", description="This router returns list of the states using pagination")
async def get_states_list(
    region_id: int,
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_states(region_id, page, limit, usr, db),
            "count": math.ceil(get_count_states(region_id, usr, db) / limit),
            "page": page,
            "limit": limit,
        }
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@state_router.post("/state/create", description="This router is able to add new state and return state id")
async def create_new_state(
    form_datas: List[NewState],
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        for form_data in form_datas:
            create_state(form_data, usr, db)

        

        raise HTTPException(status_code=200, detail="States were created successfully!")


@state_router.put("/state/{id}/update", description="This router is able to update state")
async def update_one_state(
    id: int,
    form_data: NewState,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        res = update_state(id, form_data, usr, db)
        if res:
            
            return res

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    