    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewIllness_Comment(BaseModel):
    illness_id: int
    comment: str
       
    