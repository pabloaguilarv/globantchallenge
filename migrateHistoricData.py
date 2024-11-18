import psycopg2
import pandas as pd
import os

filesPath = r'C:\Users\baste\Pablo\SSD\Dev\api-data\historicdata'

filesMap = {
    'hired_employees.csv': 'employees',
    'departments.csv': 'departments',
    'jobs.csv': 'jobs'
}

db_config = {
    "host": "challenge-challenge-globant-3b2c.k.aivencloud.com",
    "dbname": "challenge",
    "user": "avnadmin",
    "password": "AVNS_9V67I1GWUPLcMF93Bhh",
    "port": "25318"
}

db = psycopg2.connect(**db_config)
cnx = db.cursor()


def load_csv_to_postgres(csv_file, db, cnx, table_name):
    df = pd.read_csv(csv_file, header=None)

    # nombre, fecha, departamento, job

    for _, row in df.iterrows():
        if any([null for null in row.isna()]):
            insert_query = f'insert into invalidentries (employee_name, hiring_date, department_name, job_name) values (%s,%s,%s,%s)'
            data = []
            for col in row[1:]:
                try:
                    val = int(col)
                except:
                    val = col
                
                data.append(val)
            
            data = tuple(data)

        elif table_name == 'employees':
            insert_query = f"INSERT INTO {table_name} (employee_name, hiring_date, department_id, job_id)  values (%s,%s,%s,%s)"
            data = []
            for col in row[1:]:
                try:
                    val = int(col)
                except:
                    val = col
                
                data.append(val)
            
            data = tuple(data)
        elif table_name == 'departments':
            insert_query = f"INSERT INTO {table_name} (department_name) values (%s)"
            data = row[1]
        elif table_name == 'jobs':
            insert_query = f"INSERT INTO {table_name} (job_name) values (%s)"
            data = row[1]

        try:
            cnx.execute(insert_query, (data,) if not isinstance(data, tuple) else data)
        except Exception as e:
            print(table_name, data)
            raise e

        db.commit()

files = [
    'departments.csv',
    'jobs.csv',
    'hired_employees.csv'
]

for file in files:
    csv_file_path = os.path.join(filesPath, file)
    table_name = filesMap.get(file)
    load_csv_to_postgres(csv_file_path, db, cnx, table_name)

cnx.close()
db.close()