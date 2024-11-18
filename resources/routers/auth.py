from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, hashing, token
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm

get_db = database.get_db

router = APIRouter(
    tags = ['Authentication']
)

@router.post(
        '/login'
)
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.TeamMember).filter(models.TeamMember.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid Credentials'
        )
    
    if not hashing.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid Credentials'
        )
    
    access_token = token.create_access_token(
        data = {
            'sub': user.email,
        }
    )
    
    return {'access_token': access_token, 'token_type': 'bearer'}