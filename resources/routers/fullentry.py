from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, database, schemas, oauth2
from ..methods import fullentry
from sqlalchemy.orm import Session
from typing import List

get_db = database.get_db

router = APIRouter(
    prefix = '/multipleentries',
    tags = ['Multiple Entries']
)

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MultipleEntriesReponse
)
def create(
    request:schemas.MultipleEntries,
    db:Session = Depends(get_db)
):
    return fullentry.create(request, db)