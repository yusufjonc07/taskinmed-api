from app.utils import *
from app.functions.casher import *
from app.models.casher import *
from app.schemas.casher import *
import math


casher_router = APIRouter(tags=['Casher Endpoint'])

@casher_router.get("/cashers", description="This router returns list of the cashers using pagination")
async def get_cashers_list(
    user_id: int,
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        return {
            "data": get_all_cashers(user_id, page, limit, usr, db),
            "count": math.ceil(get_count_cashers(user_id, usr, db) / limit),
            "page": page,
            "limit": limit,
        }

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")



@casher_router.post("/casher/create", description="This router is able to add new casher and return casher id")
async def create_new_casher(
    form_data: NewCasher,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_casher(form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@casher_router.put("/casher/{id}/update", description="This router is able to update casher")
async def update_one_casher(
    id: int,
    form_data: NewCasher,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_casher(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    