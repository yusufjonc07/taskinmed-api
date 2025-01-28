    
from app.utils import *
from app.functions.report import *
from typing import Optional
from app.models.state import *
import math

report_router = APIRouter(tags=['Report Endpoint'])


@report_router.get("/reports", description="This router returns list of the reports using pagination")
async def get_reports_list(
    from_date: Optional[str] = now_sanavaqt.strftime("%Y-%m-01"),
    to_date: str = now_sanavaqt.strftime("%Y-%m-%d"),
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):

    if not usr.role in ['any_role']:
        return get_report_index(from_date, to_date, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@report_router.get("/state_reports", description="This router returns list of the reports using pagination")
async def get_satet_reports(
    state_id: int,
    from_date: Optional[str] = now_sanavaqt.strftime("%Y-%m-01"),
    to_date: str = now_sanavaqt.strftime("%Y-%m-%d"),
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        data = get_states_report(state_id, from_date, to_date,  page, limit, usr, db)

        return {
            "data": data,
            "count": math.ceil(get_patentsrep_count(from_date, to_date, state_id, usr, db) / limit),
            "page": page,
            "limit": limit,
            "from_date": from_date,
            "to_date": to_date,
        }

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@report_router.get("/service_reports", description="This router returns list of the reports using pagination")
async def get_serv_reports(
    service_id: int,
    from_date: Optional[str] = now_sanavaqt.strftime("%Y-%m-01"),
    to_date: str = now_sanavaqt.strftime("%Y-%m-%d"),
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        data = get_services_report(service_id, from_date, to_date,  page, limit, usr, db)

        return {
            "data": data,
            "count": math.ceil(get_servicesrep_count(from_date, to_date, service_id, usr, db) / limit),
            "page": page,
            "limit": limit,
            "from_date": from_date,
            "to_date": to_date,
        }

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
