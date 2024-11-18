from sqlalchemy.orm import Session
from .. import models, schemas, hashing
from fastapi import HTTPException, status

def create(request:schemas.Department, db:Session):
    department = db.query(models.Departments).filter(models.Departments.department_name == request.department_name)

    data = department.first()

    if data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Job with name "{request.department_name}" already exists.'
        )
    
    department = models.Departments(
        department_name = request.department_name
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def destroy(id:int, db:Session):
    department = db.query(models.Departments).filter(models.Departments.department_id == id)
    data = department.first()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f'Department with id {id} does not exists.'
        )

    department.delete(synchronize_session = False)
    db.commit()

    return 'Done'


def get_all(db:Session):
    departments = db.query(models.Departments)
    return departments


def show(id:int, db:Session):
    department = db.query(models.Departments).filter(models.Departments.department_id == id).first()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f'Department with id {id} does not exists.'
        )
    
    return department


def update(id:int, request:schemas.Department, db:Session):
    department = db.query(models.Departments).filter(models.Departments.department_id == id)
    
    if not department.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f'Department with id {id} does not exists.'
        )
    
    data = {
        'department_name': request.department_name
    }
    
    department.update(data)
    db.commit()
    return request


def get_department_id(department_name:str, db:Session):
    department_id = db.query(models.Departments).filter(models.Departments.department_name == department_name)
    
    if department_id.first():
        return department_id.first().department_id

    department = models.Departments(
        department_name = department_name
    )

    db.add(department)
    db.commit()
    db.refresh(department)
    
    return department.department_id