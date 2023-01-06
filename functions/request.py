from sqlalchemy.orm import Session
from models.request import Request
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, timedelta
import json

def insert_req(usr, method, body, req, db: Session):

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": usr.username}, expires_delta=access_token_expires
    )


    url = str(req.url)

    port_index = url.find(":6696")

    if body != 'none':
        body = json.dumps(body.__dict__)

    db.add(Request(
        token=access_token,
        method=method,  
        url=url[(port_index+5):],
        body=body
    ))

    db.commit()