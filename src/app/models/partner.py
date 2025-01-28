    
from datetime import datetime 
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean 
from sqlalchemy.orm import relationship 
from ..db import Base 
 
now_sanavaqt = datetime.now() 

class Partner(Base):
    
    __tablename__ = "partner"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    source_id = Column(Integer, ForeignKey('source.id'))
    disabled = Column(Boolean, default=False)
    upt = Column(Boolean, default=True)

    source = relationship('Source', backref='partners')
   