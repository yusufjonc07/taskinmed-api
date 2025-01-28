    
from .drug import * 
from .illness import * 
from .user import * 
from .doctor import * 

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
from ..db import Base 
 
now_sanavaqt = datetime.now() 


class Recipe_Template(Base):

    __tablename__ = "recipe_template"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    drug_id = Column(Integer, ForeignKey('drug.id'), default=0)
    illness_id = Column(Integer, ForeignKey('illness.id'), default=0)
    comment = Column(String(255), default="")
    upt = Column(Boolean, default=True)


    drug = relationship('Drug', backref='templates')
    illness = relationship('Illness', backref='templates')