from sqlalchemy.orm import Session
from .. import models, schemas, hashing
from fastapi import HTTPException, status

def create(request:schemas.Job, db:Session):
    job = db.query(models.Jobs).filter(models.Jobs.job_name == request.job_name)

    data = job.first()

    if data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Job with name "{request.job_name}" already exists.'
        )

    job = models.Jobs(
        job_name = request.job_name
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def destroy(id:int, db:Session):
    job = db.query(models.Jobs).filter(models.Jobs.job_id == id)
    data = job.first()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f'Job with id {id} does not exists.'
        )

    job.delete(synchronize_session = False)
    db.commit()

    return 'Done'


def get_all(db:Session):
    jobs = db.query(models.Jobs).all()
    return jobs


def show(id:int, db:Session):
    job = db.query(models.Jobs).filter(models.Jobs.job_id == id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f'Job with id {id} does not exists.'
        )
    
    return job


def update(id:int, request:schemas.Job, db:Session):
    job = db.query(models.Jobs).filter(models.Jobs.job_id == id)
    
    if not job.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f'Job with id {id} does not exists.'
        )
    
    data = {
        'job_name': request.job_name
    }
    
    job.update(data)
    db.commit()
    return request


def get_job_id(job_name:str, db:Session):
    job_id = db.query(models.Jobs).filter(models.Jobs.job_name == job_name)
    
    if job_id.first():
        return job_id.first().job_id
    
    job = models.Jobs(
        job_name = job_name
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    
    return job.job_id