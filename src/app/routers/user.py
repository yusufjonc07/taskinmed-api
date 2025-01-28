    
from app.utils import *
from app.functions.user import *
from app.models.user import *
from app.models.setting import *
from app.schemas.user import *
import math


user_router = APIRouter(tags=['User Endpoint'])

class MySetting(BaseModel):
    hour:float

@user_router.put("/setting_update")
async def update_setting(
    form_data: MySetting,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    db.query(Setting).update({Setting.recall_hour: form_data.hour, Setting.upt: True})
    db.commit()
    
    return "success"


@user_router.put("/minute_update")
async def update_minute(
    form_data: QueueTime,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    db.query(User).filter_by(id=usr.id).update({User.queue_time: form_data.minute, User.upt: True})
    db.commit()
    
    return "success"

@user_router.get("/settings")
async def get_setting(
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    return db.query(Setting).first()


@user_router.get("/users", description="This router returns list of the users using pagination")
async def get_users_list(
    search: Optional[str] = '',
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:

        return get_all_users(search, page, limit, usr, db)

       
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@user_router.post("/user/create", description="This router is able to add new user and return user id")
async def create_new_user(
    form_data: NewUser,
    db:Session = ActiveSession,
):
    if not usr.role in ['any_role']:
        res = create_user(form_data, usr, db)
        if res:
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@user_router.put("/user/{id}/update", description="This router is able to update user")
async def update_one_user(
    id: int,
    form_data: UpdateUser,
    db:Session = ActiveSession,
    usr: UserSchema = Depends(get_current_active_user)
):
    if not usr.role in ['any_role']:
        res = update_user(id, form_data, usr, db)
        if res:
            
            return res
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")       
    