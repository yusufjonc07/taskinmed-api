    
from models.patient import * 
from models.service import * 
from models.user import * 
from models.doctor import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from db import Base 
 
now_sanavaqt = datetime.now() 


class Queue(Base):

    __tablename__ = "queue"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), default=0)
    service_id = Column(Integer, ForeignKey('service.id'), default=0)
    number = Column(Integer, default=0)
    created_at = Column(DateTime, default=now_sanavaqt)
    updated_at = Column(DateTime, default='0000-00-00 00:00:00')
    completed_at = Column(DateTime, default='0000-00-00 00:00:00')
    date = Column(Date)
    step = Column(Integer, default=1)
    room = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), default=0)


    doctor = relationship('Doctor', backref='queues')
    patient = relationship('Patient', backref='queues')
    service = relationship('Service', backref='queues')
    user = relationship('User', backref='queues')       
    