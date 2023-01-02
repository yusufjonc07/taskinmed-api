    
from models.patient import * 
from models.service import * 
from models.user import * 
from models.doctor import * 

from datetime import datetime 
from sqlalchemy import (
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    DateTime, 
    Boolean 
)
from sqlalchemy.orm import relationship 
from db import Base 
 
now_sanavaqt = datetime.now() 


class Recall(Base):

    __tablename__ = "recall"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), default=0)
    plan_date = Column(DateTime)
    created_at = Column(DateTime, default=now_sanavaqt)
    status = Column(Boolean, default=False)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    operator_id = Column(Integer, ForeignKey('user.id'), default=0)
    talk_type = Column(String(10), nullable=True)
    queue_id = Column(Integer, ForeignKey('queue.id'), default=0)


    patient = relationship('Patient', backref='recalls')
    user = relationship('User', foreign_keys=[user_id])       
    operator = relationship('User', foreign_keys=[operator_id], backref='recalls')       
    queue = relationship('Queue',  backref='recalls')
    