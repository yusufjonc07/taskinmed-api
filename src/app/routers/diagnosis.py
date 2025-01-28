    
from app.utils import *
from app.functions.diagnosis import *
from app.models.diagnosis import *
from app.schemas.diagnosis import *
from app.functions.request import insert_req
import math


diagnosis_router = APIRouter(tags=['Diagnosis Endpoint'])


@diagnosis_router.get("/diagnosiss", description="This router returns list of the diagnosiss using pagination")
async def get_diagnosiss_list(
    page: int = 1,
    limit: int = 10,
    patient_id: int = 0,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        return {
            "data": get_all_diagnosiss(page, patient_id, limit, usr, db),
            "count": math.ceil(get_count_diagnosiss(patient_id, usr, db) / limit),
            "page": page,
            "limit": limit,
        }

        return get_all_diagnosiss(page, patient_id, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@diagnosis_router.post("/diagnosis/create", description="This router is able to add new diagnosis and return diagnosis id")
async def create_new_diagnosis(
    form_data: NewDiagnosis,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = create_diagnosis(form_data, usr, db)
        if res:
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@diagnosis_router.put("/diagnosis/{id}/update", description="This router is able to update diagnosis")
async def update_one_diagnosis(
    id: int,
    form_data: UpdateDiagnosis,
    req: Request,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_diagnosis(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    