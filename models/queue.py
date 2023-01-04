    
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
    updated_at = Column(DateTime, default=now_sanavaqt)
    completed_at = Column(DateTime, default=now_sanavaqt)
    date = Column(Date)
    step = Column(Integer, default=1)
    room = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    cancel_user_id = Column(Integer, ForeignKey('user.id'), default=0)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), default=0)
    in_room = Column(Boolean, default=False)


    doctor = relationship('Doctor',  backref='queues')
    patient = relationship('Patient', backref='queues')
    service = relationship('Service', backref='queues')
    user = relationship('User', foreign_keys=[user_id], backref='queues')       
    cancelled_user = relationship('User', foreign_keys=[cancel_user_id], backref='cancelled_queues')       
    