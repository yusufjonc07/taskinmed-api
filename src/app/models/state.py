from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class State(Base):
    __tablename__ = "state"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    region_id = Column(Integer, ForeignKey('region.id'), default=0)
    upt = Column(Boolean, default=True)

    region = relationship('Region', backref='states')       
    