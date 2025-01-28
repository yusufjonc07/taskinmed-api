from .user import * 
from sqlalchemy import Column, Integer, Numeric
from ..db import Base 
 
class Setting(Base):
    __tablename__ = "setting"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recall_hour = Column(Numeric, unique=True)
    upt = Column(Boolean, default=True)