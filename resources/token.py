from typing import Optional
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import Depends
from . import schemas
import pytz

americasTz = pytz.timezone('America/Bogota')

SECRET_KEY = 'b6254d00a20b4a6f49fe256849b3d24f91d5fb9c3bfa3b5ae410dfc7f8663d0d'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict, expires_delta:Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=americasTz) + expires_delta

    else:
        expire = datetime.now(tz=americasTz) + timedelta(minutes=15)
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        email:str = payload.get('sub')

        if email is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(email=email)
    
    except JWTError:
        raise credentials_exception