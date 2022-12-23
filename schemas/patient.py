    
from typing import List
from fastapi import UploadFile
from pydantic import BaseModel
from schemas.queue import NewQueue
from enum import Enum

class Gender(str, Enum):
    erkak = "erkak"
    ayol = "ayol"

class NewPatient(BaseModel):
    name: str
    surename: str
    fathername: str
    gender: Gender
    age: int
    address: str
    state_id: int
    region_id: int
    source_id: int
    phone: int
    queue: List[NewQueue]


class UpdatePatient(BaseModel):
    name: str
    age: int
    address: str
    state_id: int
    region_id: int
    source_id: int
    phone: int
       
    