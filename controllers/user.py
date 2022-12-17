from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends
from db import get_db
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from models.user import User
import settings
from auth import get_current_active_user

router = InferringRouter()  

@cbv(router)
class UserRot:

    db: Session = Depends(get_db)
    usr: settings.UserSchema = Depends(get_current_active_user)

    @router.get("/items")
    async def get_items(s):
        users = s.db.query(User).count()
        return users


  