from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    username: Optional[str] = None

class UserSchema(BaseModel):
    filial_id: int
    id: int
    name: str
    oylik: int
    maosh: int
    role: str
    disabled: bool


class Between(BaseModel):
    column: Optional[str] = ''
    begin: Optional[str] = ''
    end: Optional[str] = ''

class SearchData(BaseModel):
    between: Between
    search: dict
