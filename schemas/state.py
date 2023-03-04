from fastapi import HTTPException
from pydantic import BaseModel, validator
from models.state import State
from db import get_db


class NewState(BaseModel):
    name: str
    region_id: int
   