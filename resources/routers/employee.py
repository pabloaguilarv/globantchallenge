from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, database, schemas, oauth2
from ..methods import employee
from sqlalchemy.orm import Session
from typing import List


get_db = database.get_db

router = APIRouter(
    prefix = '/employee',
    tags = ['Employees']
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowEmployee
)
def create(
    request:schemas.Employee,
    db:Session = Depends(get_db)
):
    return employee.create(request, db)


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def destroy(id:int, db:Session = Depends(get_db)):
    return employee.destroy(id, db)


@router.get(
    '/{id}',
    response_model=schemas.ShowEmployee
)
def show(id:int, db:Session = Depends(get_db)):
    return employee.show(id, db)


@router.get(
    '/'
)
def all(
    db: Session = Depends(get_db),
    # get_current_user:schemas.Employee = Depends(oauth2.get_current_user)
    response_model = List[schemas.ShowEmployee]
):
    return employee.get_all(db)


@router.put(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED
)
def update(id:int, request:schemas.UpdateEmployee, db:Session = Depends(get_db)):
    return employee.update(id, request, db)