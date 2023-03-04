from pydantic import BaseModel
from enum import Enum

class Methods(str, Enum):
    naqd='naqd'
    plastik='plastik'
    otkazma='otkazma'

class NewIncome(BaseModel):
    queue_id: int
    method: Methods