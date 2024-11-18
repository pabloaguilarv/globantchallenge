from sqlalchemy.orm import Session
from .. import models, schemas, hashing
from fastapi import HTTPException, status
from .department import get_department_id
from .job import get_job_id
from datetime import datetime
import pytz

americasTz = pytz.timezone('America/Bogota')

def create(request:schemas.MultipleEntries, db:Session):
    existing:list = []
    new:list = []

    for entry in request.entries:
        exists = db.query(models.Employees).filter(models.Employees.employee_name == entry.employee_name)
        exists = exists.first()

        if exists:
            existing.append(entry.model_dump().update({'reason': 'Already Exists'}))
            continue

        if not all([entry.employee_name, entry.department_name, entry.job_name, entry.hiring_date]):
            invalid = models.InvalidEntries(
                employee_name = entry.employee_name,
                job_name = entry.job_name,
                department_name = entry.department_name,
                hiring_date = entry.hiring_date
            )

            db.add(invalid)
            db.commit()
            db.refresh(invalid)

            existing.append(
                    {
                    'employee_name': entry.employee_name,
                    'department_name': entry.department_name,
                    'job_name': entry.job_name,
                    'hiring_date': entry.hiring_date,
                    'reason': 'Missing Fields'
                }
            )

            continue

        job_id = get_job_id(entry.job_name, db)
        department_id = get_department_id(entry.department_name, db)

        newEntry = models.Employees(
            employee_name = entry.employee_name,
            job_id = job_id,
            department_id = department_id,
            hiring_date = entry.hiring_date
        )

        db.add(newEntry)
        db.commit()
        db.refresh(newEntry)

        new.append(
            {
                'employee_name': entry.employee_name,
                'department_name': entry.department_name,
                'job_name': entry.job_name,
                'hiring_date': entry.hiring_date
            }
        )

    out = {
        'newEntries': new,
        'failedEntries': existing
    }

    print(out)

    return out