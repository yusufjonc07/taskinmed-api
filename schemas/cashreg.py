    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewCashreg(BaseModel):
    name: str
       
    