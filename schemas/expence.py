from pydantic import BaseModel


class NewExpence(BaseModel):
    comment: str
    value: float
       
    