    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewService(BaseModel):
    name: str
    disabled: bool = False
       
    