from fastapi import HTTPException
from pydantic import BaseModel, validator
from app.models.state import State
from app.db import get_db


class NewState(BaseModel):
    name: str
    region_id: int
   