from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Departments(Base):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String)

    employees = relationship('Employees', back_populates='department')


class Employees(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    hiring_date = Column(String)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    job_id = Column(Integer, ForeignKey('jobs.job_id'))

    department = relationship('Departments', back_populates='employees')
    job = relationship('Jobs', back_populates='employees')


class Jobs(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String)

    employees = relationship('Employees', back_populates='job')


class InvalidEntries(Base):
    __tablename__ = 'invalidentries'

    invalid_id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    job_name = Column(String)
    department_name = Column(String)
    hiring_date = Column(String)