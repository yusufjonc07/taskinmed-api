from app.utils import *
from app.auth import get_current_active_user
from sqlalchemy.orm import joinedload
from typing import Optional, List
from app.settings import UserSchema
from app.models.partner import *
from app.models.partner_employee import *
import math
from pydantic import BaseModel

class NewPartnerEmplyees(BaseModel):
    phone: int
    name: str

class UpdatePartnerEmplyees(BaseModel):
    phone: int
    name: str
    disabled: bool = False

class NewPartner(BaseModel):
    name: str
    source_id: int
    employees: List[NewPartnerEmplyees]

class UpdatePartner(BaseModel):
    name: str
    source_id: int

partner_router = APIRouter(tags=['Partner Endpoint'])


@partner_router.get("/partners", description="This router returns list of the regions using pagination")
async def get_regions_list(
    page: int = 1,
    limit: int = 10,
    source_id: Optional[int] = 0,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        
        if page == 1 or page < 1:
            offset = 0
        else:
            offset = (page-1) * limit

        partners = db.query(Partner).options(
            joinedload(Partner.source),
            joinedload(Partner.employees)
        ).filter_by(disabled=False)

        if source_id > 0:
            partners = partners.filter_by(source_id=source_id)
        
        partners = partners.order_by(Partner.name.asc()).offset(offset).limit(limit)

        return {
            "data": partners.all(),
            "count": math.ceil(partners.count() / limit),
            "page": page,
            "limit": limit,
        }

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")




@partner_router.post("/partner/create", description="This router is able to add new region and return region id")
async def create_new_region(
    form_data: NewPartner,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        
        new_partner = Partner(
            name=form_data.name,
            source_id=form_data.source_id,
        )

        db.add(new_partner)
        db.flush()

        for p_e in form_data.employees:
            db.add(Partner_Employee(
                name=p_e.name,
                phone=p_e.phone,
                partner_id=new_partner.id
            ))
            db.flush()

        db.commit()

        raise HTTPException(status_code=200, detail="Hamkor qo'shildi!")

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@partner_router.put("/partner/{id}/update", description="This router is able to update partner")
async def update_one_region(
    id: int,
    form_data: UpdatePartner,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        
        partner = db.query(Partner).filter_by(id=id)
        this_partner = partner.first()

        if this_partner:
            partner.update({
                Partner.name: form_data.name,
                Partner.source_id: form_data.source_id
            })
            db.commit()
            raise HTTPException(status_code=200, detail="Hamkor o'zgartirildi!")
            
        else:
            raise HTTPException(status_code=400, detail="Hamkor topilmadi!")   
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       

@partner_router.post("/partner_employee/create")
async def create_new_partner_employee(
    partner_id: int,
    form_data: NewPartnerEmplyees,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        
      
        db.add(Partner_Employee(
            name=form_data.name,
            phone=form_data.phone,
            partner_id=partner_id
        ))

        db.commit()

        raise HTTPException(status_code=200, detail="Hamkorning hodimi qo'shildi!")

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@partner_router.put("/partner_employee/{id}/update", description="This router is able to update partner")
async def update_one_partner_employee(
    id: int,
    form_data: UpdatePartnerEmplyees,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        
        partner = db.query(Partner_Employee).filter_by(id=id)
        this_partner = partner.first()

        if this_partner:
            partner.update({
                Partner_Employee.name: form_data.name,
                Partner_Employee.phone: form_data.phone,
                Partner_Employee.disabled: form_data.disabled,
            })
            db.commit()
            raise HTTPException(status_code=200, detail="Hamkor o'zgartirildi!")
            
        else:
            raise HTTPException(status_code=400, detail="Hamkor topilmadi!")   
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    