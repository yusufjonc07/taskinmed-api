    
from .service import * 
from .user import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class Illness(Base):
    __tablename__ = "illness"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    service_id = Column(Integer, ForeignKey('service.id'), default=0)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)

    service = relationship('Service', backref='illnesss')
    user = relationship('User', backref='illnesss')       
    