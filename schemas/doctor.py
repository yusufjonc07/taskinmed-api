    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewDoctor(BaseModel):
    service_id: int
    cost: float
    room: int
    user_id: int
       
    