from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin_klinika:admin_klinika@185.196.214.176:3306/admin_klinika"
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Klinika#123@localhost:3306/klinika"


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


