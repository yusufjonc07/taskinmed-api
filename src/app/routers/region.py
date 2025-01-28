from app.utils import *
from app.auth import get_current_active_user
from app.settings import UserSchema
from app.functions.region import *
from app.models.region import *
from app.schemas.region import *
import math

region_router = APIRouter(tags=['Region Endpoint'])


@region_router.get("/regions", description="This router returns list of the regions using pagination")
async def get_regions_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        return {
            "data": get_all_regions(page, limit, usr, db),
            "count": math.ceil(get_count_regions(usr, db) / limit),
            "page": page,
            "limit": limit,
        }
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@region_router.post("/region/create", description="This router is able to add new region and return region id")
async def create_new_region(
    form_data: NewRegion,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_region(form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@region_router.put("/region/{id}/update", description="This router is able to update region")
async def update_one_region(
    id: int,
    form_data: NewRegion,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_region(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    