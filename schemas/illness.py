    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewIllness(BaseModel):
    name: str
    service_id: int
       
    