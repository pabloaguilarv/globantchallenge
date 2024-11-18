from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, database, schemas, oauth2
from ..methods import job
from sqlalchemy.orm import Session
from typing import List


get_db = database.get_db

router = APIRouter(
    prefix = '/job',
    tags = ['Jobs']
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Job
)
def create(
    request:schemas.Job,
    db:Session = Depends(get_db)
):
    return job.create(request, db)


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def destroy(id:int, db:Session = Depends(get_db)):
    return job.destroy(id, db)


@router.get(
    '/{id}',
    response_model=schemas.ShowJob
)
def show(id:int, db:Session = Depends(get_db)):
    return job.show(id, db)


@router.get(
    '/'
)
def all(
    db: Session = Depends(get_db),
    # get_current_user:schemas.Job = Depends(oauth2.get_current_user)
    response_model = List[schemas.ShowJob]
):
    return job.get_all(db)


@router.put(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED
)
def update(id:int, request:schemas.Job, db:Session = Depends(get_db)):
    return job.update(id, request, db)