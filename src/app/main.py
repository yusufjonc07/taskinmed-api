from fastapi.middleware.cors import CORSMiddleware
from .auth import auth_router
from .routes import routes
from .gii import gii_router
from .wsroutes import queue_ws
from fastapi import FastAPI, File
import uvicorn
from app.db import Base, engine
from .schemas.user import NewUser
from .functions.user import create_user
from sqlalchemy.orm import Session
from .db import ActiveSession



app = FastAPI(
    title= "MEDIC",
    description="This project consists of so many functions \n  for operating proccess in the medical centres.",
    contact={
        'name': 'CRUD group',
        'url': 'https://onlyup.uz',
        'email': 'ahmedovyusufjon3@gmail.com'
    },
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def start():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(e)

@app.get("/")
async def get():

    return 'Kilinika'

@auth_router.post("/user/signup", description="This router is able to add new user and return user id")
async def create_new_user(
    form_data: NewUser,
    db:Session = ActiveSession,
):
    return create_user(form_data, None, db)

app.include_router(gii_router)
app.include_router(auth_router)
app.include_router(queue_ws)
app.include_router(routes)

def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8778, log_level="debug", reload=True)
    
