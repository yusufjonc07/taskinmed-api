    
from app.utils import *
from app.functions.doctor import *
from app.models.doctor import *
from app.schemas.doctor import *
import math

doctor_router = APIRouter(tags=['Doctor Endpoint'])


@doctor_router.get("/doctors", description="This router returns list of the doctors using pagination")
async def get_doctors_list(
    user_id: Optional[int] = 0,
    service_id: Optional[int] = 0,
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        return {
            "data": get_all_doctors(user_id, service_id, page, limit, usr, db),
            "count": math.ceil(get_count_doctors(user_id, service_id, usr, db) / limit),
            "page": page,
            "limit": limit,
        }

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@doctor_router.post("/doctor/create", description="This router is able to add new doctor and return doctor id")
async def create_new_doctor(
    form_data: NewDoctor,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_doctor(form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@doctor_router.put("/doctor/{id}/update", description="This router is able to update doctor")
async def update_one_doctor(
    id: int,
    form_data: NewDoctor,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_doctor(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    