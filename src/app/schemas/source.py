from fastapi import HTTPException
from pydantic import BaseModel, validator
from app.models.source import Source
from app.db import get_db


class NewSource(BaseModel):
    name: str
    # @validator('name')
    # def unique_name(cls: BaseModel, v: str) -> str:
    #     db = next(get_db())
    #     users = db.query(Source).all()
    #     db.commit()
    #     if str(v) in set(map(lambda u: u.name, users)):
    #         raise HTTPException(status_code=400, detail='Nom raqam allaqachon foydalanilgan')
    #     return v