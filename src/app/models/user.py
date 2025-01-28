    

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    role = Column(String, default='')
    phone = Column(Integer, unique=True)
    queue_time = Column(Integer, default=0)
    created_at = Column(DateTime, default=now_sanavaqt)
    updated_at = Column(DateTime, default=now_sanavaqt)
    username = Column(String, default='')
    password_hash = Column(String, default='')
    disabled = Column(Boolean, default=False)
    upt = Column(Boolean, default=True)
    