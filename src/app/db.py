from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = "postgresql://root:root@database:5432/clinic"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

ActiveSession = Depends(get_db)

class  MyCrazy:
    def __call__(self) -> None:
        self._db: Session = ActiveSession


