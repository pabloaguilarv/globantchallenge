import requests
import json
from datetime import datetime
import pandas as pd
import os

baseUrl = 'http://127.0.0.1:8000/'
route = 'multipleentries'

entries = [
    {
        'employee_name': 'Julio',
        'job_name': 'Data Engineer',
        'department_name': 'Engineering',
        # 'hiring_date': '2024/11/11'
    },
    # {
    #     'employee_name': 'Pablo',
    #     'job_name': 'Data Engineer',
    #     'department_name': 'Engineering',
    #     'hiring_date': '2024/11/11'
    # },
    # {
    #     'employee_name': 'Jose',
    #     'job_name': 'Data Engineer',
    #     'department_name': 'Engineering',
    #     'hiring_date': '2024/11/11'
    # },
    # {
    #     'employee_name': 'Jenny',
    #     'job_name': 'Data Engineer',
    #     'department_name': 'Engineering',
    #     'hiring_date': '2024/11/11'
    # },
    # {
    #     'employee_name': 'Juan',
    #     'job_name': 'Data Engineer',
    #     'department_name': 'Engineering',
    #     'hiring_date': '2024/11/11'
    # }
]

headers = {"Content-Type": "application/json"}

parameters = {
  'entries': entries
}

fullUrl = baseUrl + route

# resp = requests.post(
#     fullUrl,
#     json=parameters,
#     headers=headers
# )

# print(resp.text)

filesPath = r'C:\Users\baste\Pablo\SSD\Dev\api-data\historicdata\hired_employees.csv'

data = pd.read_csv(filesPath, header=None)

for _, row in data.head().iterrows():
    # print(any([null for null in row.isna()]))
    print(row)
