    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewState(BaseModel):
    name: str
    region_id: int
       
    