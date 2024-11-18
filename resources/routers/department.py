from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, database, schemas
from ..methods import department
from sqlalchemy.orm import Session
from typing import List

get_db = database.get_db

router = APIRouter(
    prefix = '/department',
    tags = ['Departments']
)

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowDepartment
)
def create(request:schemas.Department, db:Session = Depends(get_db)):
    return department.create(request, db)


@router.get(
    '/',
    response_model=List[schemas.ShowDepartment]
)
def all(db:Session = Depends(get_db)):
    return department.get_all(db)


@router.delete(
    '/',
    status_code=status.HTTP_204_NO_CONTENT
)
def destroy(id:int, db:Session = Depends(get_db)):
    return department.destroy(id, db)


@router.get(
    '/{id}',
    response_model=schemas.ShowDepartment
)
def show(id:int, db:Session = Depends(get_db)):
    return department.show(id, db)


@router.put(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Department
)
def update(id:int, request:schemas.Department, db:Session = Depends(get_db)):
    return department.update(id, request, db)