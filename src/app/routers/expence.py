from app.utils import *
from app.functions.expence import *
from app.models.expence import *
from app.schemas.expence import *
import math
from typing import Optional

expence_router = APIRouter(tags=['Expence Endpoint'])


@expence_router.get("/expences", description="This router returns list of the expences using pagination")
async def get_expences_list(
    from_date: Optional[str] = now_sanavaqt.strftime("%Y-%m-01"),
    to_date: str = now_sanavaqt.strftime("%Y-%m-%d"),
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = '',
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_expences(search, from_date, to_date, page, limit, usr, db),
            "count": math.ceil(get_count_expences(search, from_date, to_date, usr, db) / limit),
            "page": page,
            "limit": limit,
        }

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@expence_router.post("/expence/create", description="This router is able to add new expence and return expence id")
async def create_new_expence(
    form_data: NewExpence,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_expence(form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@expence_router.put("/expence/{id}/update", description="This router is able to update expence")
async def update_one_expence(
    id: int,
    req: Request,
    form_data: NewExpence,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_expence(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    