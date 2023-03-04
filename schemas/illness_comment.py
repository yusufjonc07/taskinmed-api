    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewIllness_Comment(BaseModel):
    service_id: int
    comment: str
       
    