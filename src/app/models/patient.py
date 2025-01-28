from .state import * 
from .region import * 
from .source import * 
from .user import * 
from .partner import * 
from .partner_employee import * 
from sqlalchemy.orm import backref

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    surename = Column(String, default='')
    fathername = Column(String, default='')
    gender = Column(String, default='unknown')
    age = Column(Date)
    address = Column(String, default='')
    state_id = Column(Integer, ForeignKey('state.id'), default=0)
    region_id = Column(Integer, ForeignKey('region.id'), default=0)
    source_id = Column(Integer, ForeignKey('source.id'), default=0)
    partner_employee_id = Column(Integer, ForeignKey('partner_employee.id'), default=0)
    partner_id = Column(Integer, ForeignKey('partner.id'), default=0)
    phone = Column(Integer,  unique=True)
    created_at = Column(DateTime, default=now_sanavaqt)
    updated_at = Column(DateTime, default=now_sanavaqt)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    upt = Column(Boolean, default=True)

    state = relationship('State', backref='patients', lazy="joined")
    region = relationship('Region', backref='patients', lazy="joined")
    source = relationship('Source', backref='patients')
    user = relationship('User', backref='patients')       
    partner = relationship('Partner', backref='patients')       
    partner_employee = relationship('Partner_Employee', backref='patients')       
    