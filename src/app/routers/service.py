    
from app.utils import *
from app.functions.service import *
from app.models.service import *
from app.schemas.service import *
from typing import List
import math

service_router = APIRouter(tags=['Service Endpoint'])


@service_router.get("/services", description="This router returns list of the services using pagination")
async def get_services_list(
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_services(page, limit, usr, db),
            "count": math.ceil(get_count_services(usr, db) / limit),
            "page": page,
            "limit": limit,
        }
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@service_router.post("/service/create", description="This router is able to add new service and return service id")
async def create_new_service(
    form_datas: List[NewService],
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        for form_data in form_datas:
            create_service(form_data, usr, db)

        
        
        raise HTTPException(status_code=200, detail="Success!")
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@service_router.put("/service/{id}/update", description="This router is able to update service")
async def update_one_service(
    id: int,
    form_data: UpdateService,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_service(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    