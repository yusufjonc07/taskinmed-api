    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewDiagnosis(BaseModel):
    illness: str
    description: str
    user_id: int
    queue_id: int
       
    