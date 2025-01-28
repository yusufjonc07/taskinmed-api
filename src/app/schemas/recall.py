    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from enum import Enum

class TalkType(str, Enum):
    ijobiy="ijobiy"
    salbiy="salbiy"
    etiroz="etiroz"

class NewRecall(BaseModel):
    patient_id: int
    plan_date: str

class UpdateRecall(BaseModel):
    plan_date: str

class TalkedRecall(BaseModel):
    comment: str
    talk_type: TalkType
       
    