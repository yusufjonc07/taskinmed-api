    
from typing import Optional, List
from app.schemas.recipe import NewRecipe
from pydantic import BaseModel


class NewDiagnosis(BaseModel):
    illness: str
    description: Optional[str] = ''
    queue_id: int
    recipes: List[NewRecipe]


class UpdateDiagnosis(BaseModel):
    illness: str
    description: Optional[str] = ''


       
    