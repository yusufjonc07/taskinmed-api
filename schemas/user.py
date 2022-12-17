    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from enum import Enum
from pydantic import Field

class UserRoles(str, Enum):
    admin='admin'
    operator='operator'
    reception='reception'
    doctor='doctor'
    casher='casher'

class NewUser(BaseModel):
    name: str
    role: UserRoles
    phone: int
    username: str = Field(min_length=5)
    password_hash: Optional[str] = Field(min_length=8, default='')
    disabled: bool

class UpdateUser(BaseModel):
    name: str
    role: UserRoles
    phone: int
    username: str = Field(min_length=5)
    password_hash: Optional[str] = ''
    disabled: bool



       
    