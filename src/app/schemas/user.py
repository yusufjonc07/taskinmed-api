from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, validator
from enum import Enum
from pydantic import Field
from app.models.user import User
from app.db import get_db

class UserRoles(str, Enum):
    admin='admin'
    operator='operator'
    reception='reception'
    doctor='doctor'
    casher='casher'

class QueueTime(BaseModel):
    minute: int

class NewUser(BaseModel):
    name: str
    role: UserRoles
    phone: int
    username: str = Field(min_length=5)
    password_hash: Optional[str] = Field(min_length=8, default='')
    disabled: bool

    @validator('username')
    def unique_name(cls: BaseModel, v: str) -> str:
        db = next(get_db())
        users = db.query(User).all()
        db.commit()
        if str(v) in set(map(lambda u: u.username, users)):
            raise HTTPException(status_code=400, detail='Login allaqachon foydalanilgan')
        return v

    @validator('phone')
    def unique_phone(cls: BaseModel, v: str) -> str:
        db = next(get_db())
        users = db.query(User).all()
        db.commit()
        if str(v) in set(map(lambda u: u.phone, users)):
            raise HTTPException(status_code=400, detail='Telefon raqam allaqachon foydalanilgan')
        return v

class UpdateUser(BaseModel):
    name: str
    role: UserRoles
    phone: int
    username: str = Field(min_length=5)
    password_hash: Optional[str] = ''
    disabled: bool



       
    