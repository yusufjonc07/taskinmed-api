from .service import * 
from .user import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship
from ..db import Base 
 
now_sanavaqt = datetime.now() 

class Doctor(Base):
    
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey('service.id'), default=0)
    room = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    cost = Column(Numeric, default=0)
    flat = Column(Numeric, default=1)
    upt = Column(Boolean, default=True)

    service = relationship('Service', backref='doctors')
    user = relationship('User', backref='doctors', lazy="joined")       
    