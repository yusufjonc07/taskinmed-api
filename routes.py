
from fastapi import APIRouter, Depends
from auth import get_current_active_user
from routers.patient import patient_router
from routers.source import source_router
from routers.diagnosis import diagnosis_router
from routers.queue import queue_router
from routers.region import region_router
from routers.service import service_router
from routers.state import state_router
from routers.user import user_router
from routers.drug import drug_router
from routers.doctor import doctor_router
from routers.cashreg import cashreg_router
from routers.casher import casher_router
from routers.income import income_router
from routers.report import report_router
from routers.expence import expence_router

ActiveUser = Depends(get_current_active_user)
routes = APIRouter(dependencies=[ActiveUser])


routes.include_router(report_router)      
routes.include_router(expence_router)      
routes.include_router(income_router)      
routes.include_router(cashreg_router)       
routes.include_router(casher_router)       
routes.include_router(patient_router)
routes.include_router(source_router)
routes.include_router(diagnosis_router)
routes.include_router(queue_router)
routes.include_router(region_router)
routes.include_router(service_router)
routes.include_router(state_router)
routes.include_router(user_router)
routes.include_router(drug_router)       
routes.include_router(doctor_router)       
