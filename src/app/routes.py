
from fastapi import APIRouter, Depends
from app.auth import get_current_active_user
from app.routers.patient import patient_router
from app.routers.source import source_router
from app.routers.diagnosis import diagnosis_router
from app.routers.queue import queue_router
from app.routers.region import region_router
from app.routers.service import service_router
from app.routers.state import state_router
from app.routers.user import user_router
from app.routers.drug import drug_router
from app.routers.doctor import doctor_router
from app.routers.cashreg import cashreg_router
from app.routers.casher import casher_router
from app.routers.income import income_router
from app.routers.report import report_router
from app.routers.expence import expence_router
from app.routers.recipe import recipe_router
from app.routers.recall import recall_router
from app.routers.illness import illness_router
# from routers.illness_comment import illness_comment_router
from app.routers.recipe_template import recipe_template_router
from app.routers.partner import partner_router



ActiveUser = Depends(get_current_active_user)

routes = APIRouter(dependencies=[ActiveUser])


routes.include_router(partner_router)
routes.include_router(recipe_template_router)
routes.include_router(recall_router)      
routes.include_router(report_router)      
routes.include_router(expence_router)      
routes.include_router(recipe_router)      
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
routes.include_router(illness_router)       
# routes.include_router(illness_comment_router)       
