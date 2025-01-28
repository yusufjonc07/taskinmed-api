    
from .user import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    disabled = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    upt = Column(Boolean, default=True)

    user = relationship('User', backref='services')       
    