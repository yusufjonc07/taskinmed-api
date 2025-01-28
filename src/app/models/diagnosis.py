    
from .user import * 
from .queue import * 
from .patient import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class Diagnosis(Base):
    __tablename__ = "diagnosis"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    illness = Column(String, default='')
    description = Column(String, default='')
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    queue_id = Column(Integer, ForeignKey('queue.id'), default=0)
    patient_id = Column(Integer, ForeignKey('patient.id'), default=0)
    created_at = Column(DateTime, default=now_sanavaqt)
    updated_at = Column(DateTime, default=now_sanavaqt)
    upt = Column(Boolean, default=True)

    user = relationship('User', backref='diagnosiss')
    patient = relationship('Patient', backref='diagnosiss')
    queue = relationship('Queue', backref='diagnosiss')       
    