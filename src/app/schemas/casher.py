    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class NewCasher(BaseModel):
    user_id: int
    cashreg_id: int
    disabled: bool
       
    