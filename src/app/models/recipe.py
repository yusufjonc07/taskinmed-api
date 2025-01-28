    
from .user import * 
from .drug import * 
from .patient import * 
from .queue import * 
from .diagnosis import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    drug_id = Column(Integer, ForeignKey('drug.id'), default=0)
    patient_id = Column(Integer, ForeignKey('patient.id'), default=0)
    queue_id = Column(Integer, ForeignKey('queue.id'), default=0)
    diagnosis_id = Column(Integer, ForeignKey('diagnosis.id'), default=0)
    created_at = Column(DateTime, default=now_sanavaqt)
    comment = Column(String)
    upt = Column(Boolean, default=True)

    # day = Column(Integer, default=0)
    # time = Column(Integer, default=0)
    # meal = Column(Integer, default=0)
    # method = Column(String, default='tabletka')
    # duration = Column(Numeric, default=0)
    # unit = Column(Numeric, default=0)

    user = relationship('User', backref='recipes')
    drug = relationship('Drug', backref='recipes')
    patient = relationship('Patient', backref='recipes')
    queue = relationship('Queue', backref='recipes')
    diagnosis = relationship('Diagnosis', backref='recipes')       
    