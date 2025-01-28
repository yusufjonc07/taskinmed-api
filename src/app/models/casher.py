    
from .user import * 
from .cashreg import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from app.db import Base 
 
now_sanavaqt = datetime.now() 


class Casher(Base):
    __tablename__ = "casher"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    cashreg_id = Column(Integer, ForeignKey('cashreg.id'), default=0)
    disabled = Column(Boolean, default=False)
    upt = Column(Boolean, default=True)

    user = relationship('User', backref='cashers')
    cashreg = relationship('Cashreg', backref='cashers')       
    