from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, database, schemas, oauth2
from ..methods import backup
from sqlalchemy.orm import Session
from typing import List
import os

get_db = database.get_db

router = APIRouter(
    prefix = '/backup',
    tags = ['Backup']
)

@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
)
def create(
    request:schemas.Backup,
    db:Session = Depends(get_db)
):
    return backup.create(request, db)

@router.post(
    '/restore',
    status_code=status.HTTP_201_CREATED
)
def restore(
    request:schemas.Backup,
    db:Session = Depends(get_db)
):
    return backup.restore(request, db)