from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from .job import get_job_id
from .department import get_department_id


def create(request:schemas.Employee, db:Session):
    employee = db.query(models.Employees).filter(models.Employees.employee_name == request.employee_name)

    data = employee.first()

    if data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Employee with name "{request.employee_name}" already exists. With id {data.employee_id}'
        )
    
    job_id = get_job_id(request.job_name, db)
    department_id = get_department_id(request.department_name, db)
    
    new_employee = models.Employees(
        employee_name = request.employee_name,
        hiring_date = request.hiring_date,
        department_id = department_id,
        job_id = job_id
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def destroy(id:int, db:Session):
    employee = db.query(models.Employees).filter(models.Employees.employee_id == id)
    data = employee.first()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee does not exist."
        )

    employee.delete(synchronize_session=False)
    db.commit()

    return 'Done'


def show(id:int, db:Session):
    employee = (db.query(
        models.Employees
    )
                .filter(models.Employees.employee_id == id)
                .join(models.Employees.department)
                .join(models.Employees.job))

    print(employee)

    employee = employee.first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Employee with id {id} does not exist.'
        )

    return employee


def get_all(db:Session):
    employees = db.query(models.Employees).all()
    return employees


def update(id:int, request:schemas.UpdateEmployee, db:Session):
    employee = db.query(models.Employees).filter(models.Employees.employee_id == id)

    if not employee.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Employee with id {id} does not exist.'
        )
    
    data = {
        'message': 'Successfully updated',
        'employee_id': id,
        'employee_name': request.employee_name,
        'employee_department': request.department_id,
        'employee_job': request.job_id,
        'hiring_date': request.hiring_date
    }

    employee.update(request.model_dump())
    db.commit()
    return data