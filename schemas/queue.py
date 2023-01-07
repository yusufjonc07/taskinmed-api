    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from enum import Enum



class NewQueue(BaseModel):
    doctor_id: int
    service_id: int
    room: int
    time: str
       
    