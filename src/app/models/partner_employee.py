    
from .partner import * 
from datetime import datetime 
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 

class Partner_Employee(Base):
    
    __tablename__ = "partner_employee"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    phone = Column(Integer)
    partner_id = Column(Integer, ForeignKey('partner.id'))
    disabled = Column(Boolean, default=False)
    upt = Column(Boolean, default=True)

    partner = relationship('Partner', backref='employees')
   