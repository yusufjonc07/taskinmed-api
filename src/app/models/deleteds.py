from sqlalchemy import Column, Integer, String, Boolean
from ..db import Base 


class Deleteds(Base):
    __tablename__ = "deleteds"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table = Column(String)
    item_id = Column(Integer)
    upt = Column(Boolean, default=False)

    