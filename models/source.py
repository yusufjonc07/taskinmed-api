    

from datetime import datetime 
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean 
from sqlalchemy.orm import relationship 
from db import Base 
 
now_sanavaqt = datetime.now() 


class Source(Base):
    __tablename__ = "source"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
       
    