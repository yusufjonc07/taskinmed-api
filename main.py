from fastapi.middleware.cors import CORSMiddleware
from gii import gii_router
from auth import auth_router
from routes import routes
from fastapi import FastAPI
from wsroutes import queue_ws

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


@app.get("/")
async def get():

    return 'Kilinika'



app.include_router(gii_router)
app.include_router(auth_router)
app.include_router(routes)
app.include_router(queue_ws)

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(
#         app,
#         host='localhost',
#         port=8778,
#         reload=True
#     )