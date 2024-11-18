import fastavro.read
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from datetime import datetime
import pytz
import fastavro
import os

americasTz = pytz.timezone('America/Bogota')

def create(request:schemas.Backup, db:Session):
    for table in request.tables:
        workingDirectory = os.getcwd()

        backupPath = workingDirectory + f'\\backup\\{table}\\'

        backupTime = datetime.now(tz=americasTz).strftime('%Y-%m-%d_%H:%M:%S')

        if table.lower() == 'employees':
            schema = {
                'type': 'record',
                'name': table,
                'fields': [
                    {'name': 'employee_id', 'type': 'int'},
                    {'name': 'employee_name', 'type': 'string'},
                    {'name': 'hiring_date', 'type': 'string'},
                    {'name': 'department_id', 'type': 'int'},
                    {'name': 'job_id', 'type': 'int'},
                ]
            }

            tableData = db.query(models.Employees).all()
            
            tableData = [dict(row.__dict__) for row in tableData]

            print(tableData)

        elif table.lower() == 'departments':
            schema = {
                'type': 'record',
                'name': table,
                'fields': [
                    {'name': 'department_id', 'type': 'int'},
                    {'name': 'department_name', 'type': 'string'}
                ]
            }

            tableData = db.query(models.Departments).all()

        elif table.lower() == 'jobs':
            schema = {
                'type': 'record',
                'name': table,
                'fields': [
                    {'name': 'job_id', 'type': 'int'},
                    {'name': 'job_name', 'type': 'string'},
                ]
            }

            tableData = db.query(models.Jobs).all()
        
        else:
            return HTTPException(status.HTTP_404_NOT_FOUND, detail='Table to backup does not exists.')
        
        writingPath = os.path.join(backupPath, f'backup-{table}-{backupTime}.avro')

        try:
            os.makedirs(backupPath)
        except:
            pass

        with open(writingPath, 'wb') as file:
            fastavro.writer(file, schema, tableData)


def restore(request:schemas.Backup, db:Session):
    for table in request.tables:
        workingDirectory = os.getcwd()

        backupPath = workingDirectory + f'/backup/{table}/'

        lastBackups = max(os.listdir(backupPath))

        filePath = backupPath + lastBackups + '.avro'

        print(filePath)

        with open(filePath, 'rb') as file:
            reader = fastavro.reader(file)
            schema = reader.schema

            insertQuery = f'insert into {table} (%s) values (%s)'
            cols = ', '.join(field['name'] for field in schema['fields'])
            insertQuery = insertQuery % (cols, '%s')

            for record in reader:
                db.execute(insertQuery, tuple(record.values()))
                db.commit()