from fastapi import HTTPException
from pydantic import BaseModel, validator
from models.state import State
from db import get_db


class NewState(BaseModel):
    name: str
    region_id: int
    @validator('name')
    def unique_name(self, cls: BaseModel, v: str) -> str:
        db = next(get_db())
        users = db.query(State).filter_by(region_id=self.region_id).all()
        db.commit()
        if str(v) in set(map(lambda u: u.name, users)):
            raise HTTPException(status_code=400, detail='Nom raqam allaqachon foydalanilgan')
        return v