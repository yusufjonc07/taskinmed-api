    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewRegion(BaseModel):
    name: str
       
    