    
from .patient import * 
from .queue import * 
from .user import * 
from .cashreg import * 
from datetime import datetime 
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, DateTime 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 

class Expence(Base):
    
    __tablename__ = "expence"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(Numeric, default=0)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    created_at = Column(DateTime, default=now_sanavaqt)
    comment = Column(String)
    upt = Column(Boolean, default=True)

    user = relationship('User', backref='expences')
    