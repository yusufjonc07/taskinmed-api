    
from typing import List
from fastapi import HTTPException
from pydantic import BaseModel, validator
from app.schemas.queue import NewQueue
from app.models.patient import Patient
from enum import Enum
from app.db import get_db

class Gender(str, Enum):
    erkak = "erkak"
    ayol = "ayol"

class NewPatient(BaseModel):
    name: str
    surename: str
    fathername: str
    age: str
    address: str
    state_id: int
    region_id: int
    source_id: int
    partner_id: int
    partner_employee_id: int
    phone: int
    queue: List[NewQueue]

    @validator('phone')
    def unique_phone(cls: BaseModel, v: int) -> int:
        db = next(get_db())
        users = db.query(Patient).filter_by(phone=v).first()
        if users:
            raise HTTPException(status_code=400, detail='Telefon raqam allaqachon foydalanilgan')
        return v


class UpdatePatient(BaseModel):
    name: str
    surename: str
    fathername: str
    age: str
    address: str
    state_id: int
    region_id: int
    source_id: int
    partner_id: int
    partner_employee_id: int
    phone: int

class PhoneUnique(BaseModel):
    phone: int
       
    