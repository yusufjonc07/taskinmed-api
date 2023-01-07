import threading
from sqlalchemy.orm import Session
from db import engine
from models.request import Request
import requests

def doSomething():
    with Session(engine) as session:
        reqs = session.query(Request).filter_by(status=False).all()


        for req in reqs:
            url = "http://192.168.0.138" + req.url
            headers = {
                "accept": "application/json",
                "Authourization": "Bearer " + req.token,
                "Content-Type": "application/json",
            }

            if req.method == 'post':
                res = requests.post(
                    url=url,
                    headers=headers,
                    data=req.body
                )

                if res:
                    print("OK")
                else:
                    print("error")





def set_interval(func, sec): 
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

t = set_interval(lambda: doSomething, 5)
# ...
t.stop()
