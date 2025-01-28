    
from .service import * 

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class Illness_Comment(Base):
    __tablename__ = "illness_comment"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey('service.id'), default=0)
    comment = Column(String, default='')

    service = relationship('Service', backref='illness_comments')       
    