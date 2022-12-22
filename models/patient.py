    
from models.state import * 
from models.region import * 
from models.source import * 
from models.user import * 
from sqlalchemy.orm import backref

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from db import Base 
 
now_sanavaqt = datetime.now() 


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    age = Column(Integer, default=0)
    address = Column(String, default='')
    state_id = Column(Integer, ForeignKey('state.id'), default=0)
    region_id = Column(Integer, ForeignKey('region.id'), default=0)
    source_id = Column(Integer, ForeignKey('source.id'), default=0)
    phone = Column(Integer, default=0)
    created_at = Column(DateTime, default=now_sanavaqt)
    updated_at = Column(DateTime, default=now_sanavaqt)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)

    state = relationship('State', backref='patients')
    region = relationship('Region', backref='patients')
    source = relationship('Source', backref='patients')
    user = relationship('User', backref='patients')       
    