    
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from enum import Enum

class Methods(str, Enum):
    tabletka = "tabletka"
    ukol = "ukol"
    sistema = "sistema"


class NewRecipe(BaseModel):
    drug_id: int
    unit: str
       
    