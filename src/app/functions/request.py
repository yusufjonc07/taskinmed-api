from sqlalchemy.orm import Session
from app.models.request import Request
from app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, timedelta
import json

def insert_req(req, usr, method, body, db: Session):

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": usr.username}, expires_delta=access_token_expires
    )


    url = str(req.url)

    port_index = url.find(":6696")


    db.add(Request(
        token=access_token,
        method=method,  
        url=url[(port_index+5):],
        body=json.dumps(body.dict())
    ))

    db.commit()