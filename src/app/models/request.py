from sqlalchemy import Column,  Integer, String, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT 
from sqlalchemy.orm import relationship 
from ..db import Base 


class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, default="none")
    method = Column(String, default="none")
    url = Column(String, default="none")
    body = Column(String, default="none")
    status = Column(Boolean, default=False)
    upt = Column(Boolean, default=True)
    