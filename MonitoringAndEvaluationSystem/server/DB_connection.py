# Method-2: use Cloud

import pyodbc

server = 'monitoring-and-evaluation-db.database.windows.net'
database = 'Monitoring-and-Evaluation-System-DB'
username = 'DBadministrator'
password = 'UPMers2024'
driver = '{ODBC Driver 18 for SQL Server}'

try:
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server +
                          ';DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = conn.cursor()
    print("Connected to database successfully")
except Exception as e:
    print("Error connecting to database: ", e)
