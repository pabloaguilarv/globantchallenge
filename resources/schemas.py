from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    email:Optional[str] = None


class Employee(BaseModel):
    employee_name:str
    hiring_date:str
    department_name:str
    job_name:str

    class Config:
        from_attributes = True


class Department(BaseModel):
    department_name:str

    class Config:
        from_attributes = True


class Job(BaseModel):
    job_name:str

    class Config:
        from_attributes = True


class ShowEmployee(BaseModel):
    employee_id:int
    employee_name:str
    hiring_date:str
    job_id:int
    department_id:int


class UpdateEmployee(BaseModel):
    employee_name:str
    job_id:int
    department_id:int
    hiring_date:str

class ShowDepartment(BaseModel):
    department_id:int
    department_name:str


class ShowJob(BaseModel):
    job_id:int
    job_name:str


class UpdateEmployeeByNames(BaseModel):
    employee_name:str
    department_name:str
    job_name:str
    hiring_date:str

    class Config():
        from_attributes = True


class UpdateEmployeeByIds(BaseModel):
    employee_id:str
    department_id:str
    job_id:str
    hiring_date:str

    class Config():
        from_attributes = True


class FullEntry(BaseModel):
    employee_name:Optional[str] = None
    department_name:Optional[str] = None
    job_name:Optional[str] = None
    hiring_date:Optional[str] = None
    reason:Optional[str] = None


class MultipleEntries(BaseModel):
    entries: List[FullEntry]


class MultipleEntriesReponse(BaseModel):
    newEntries: List[FullEntry]
    failedEntries: List[FullEntry]


class InvalidEntries(BaseModel):
    employee_name:str
    job_name:str
    department_name:str
    hiring_date:str


class Backup(BaseModel):
    tables:List[str]