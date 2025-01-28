    
from .patient import * 
from .queue import * 
from .user import * 
from .cashreg import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class Income(Base):
    
    __tablename__ = "income"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(Numeric, default=0)
    patient_id = Column(Integer, ForeignKey('patient.id'), default=0)
    queue_id = Column(Integer, ForeignKey('queue.id'), default=0)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    cashreg_id = Column(Integer, ForeignKey('cashreg.id'), default=0)
    created_at = Column(DateTime, default=now_sanavaqt)
    updated_at = Column(DateTime, default=now_sanavaqt)
    taken = Column(Boolean, default=False)
    method = Column(String, default="naqd")
    upt = Column(Boolean, default=True)

    patient = relationship('Patient', backref='incomes')
    queue = relationship('Queue', backref='incomes')
    user = relationship('User', backref='incomes')
    cashreg = relationship('Cashreg', backref='incomes')       
    