from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class NewQueue(BaseModel):
    doctor_id: int
    service_id: int
    room: int
    time: str
    date: Optional[str] = datetime.now().strftime("%Y-%m-%d")
       
    