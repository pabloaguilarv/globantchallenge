from fastapi import FastAPI, Depends, HTTPException
from resources import schemas, models, database
from sqlalchemy.orm import Session
from resources.routers import department, employee, auth, job, fullentry, backup

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(fullentry.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(job.router)
app.include_router(auth.router)
app.include_router(backup.router)