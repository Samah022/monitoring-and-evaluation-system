from datetime import datetime, timedelta

from ..evaluationCriteriaManagement.uniformEntity import Uniform
import sqlite3


class UniformDB:
    def __init__(self):
        self.__uniform_obj = Uniform()

    """
    Retrieves the current data from the "Uniform" table in the database.

    Args:
        cursor (database cursor): The database cursor object used for executing SQL queries.

    Returns:
        list of dictionaries or None: The retrieved data as a list of dictionaries, where each dictionary represents a row of data with the following keys:
            - "label" (str): The compliance label.
            - "value" (int): The total amount for the compliance label.
            The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'label': 'Compliant', 'value': 10}, {'label': 'NonCompliant', 'value': 5}]
    """

    def get_current_data(self, cursor):
        try:
            data = []

            sql_query = """
            SELECT Compliance, SUM(Amount) AS TotalAmount 
            FROM Uniform 
            WHERE strftime('%H:%M', Timestamp) = strftime('%H:%M', datetime('now', 'localtime'))
            GROUP BY Compliance;
            """

            cursor.execute(sql_query)
            rows = cursor.fetchall()

            for row in rows:
                data.append({
                    "label": row[0],
                    "value": row[1]
                })

            return data

        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False

    """
    Retrieves data for a specific month of the current year from the "Uniform" table in the database.

    Args:
        cursor (database cursor): The database cursor object used for executing SQL queries.

    Returns:
        list of dictionaries or None: The retrieved data as a list of dictionaries, where each dictionary represents a row of data with the following keys:
            - "time" (str): The formatted timestamp of the data in the format "%Y-%m-%d %H:%M:%S".
            - "Compliant" (int): The amount of compliant data.
            - "NonCompliant" (int): The amount of non-compliant data.
            The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'time': '2024-01-01 12:30:45', 'Compliant': 10, 'NonCompliant': 5}, {'time': '2024-02-02 08:15:20', 'Compliant': 5, 'NonCompliant': 2}]
    """

    def get_month_data(self, cursor):

        try:
            current_year = datetime.now().year
            data = []

            sql_query = """ 
                SELECT *
                FROM Uniform
                WHERE Timestamp BETWEEN ? AND ?; 
            """
            start_of_year = f"{current_year}-01-01 00:00:00"
            end_of_year = f"{current_year}-12-31 23:59:59"

            cursor.execute(sql_query, (start_of_year, end_of_year))
            rows = cursor.fetchall()

            for row in rows:
                timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                Compliant_amount = 0
                NonCompliant_amount = 0

                if row[1] == "Compliant":
                    Compliant_amount = row[2]
                elif row[1] == "NonCompliant":
                    NonCompliant_amount = row[2]

                data.append({
                    "time": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "Compliant": Compliant_amount,
                    "NonCompliant": NonCompliant_amount,
                })

            return data

        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False

    """
    Retrieves data for the current day from the "Uniform" table in the database.

    Args:
        cursor (database cursor): The database cursor object used for executing SQL queries.

    Returns:
        list of dictionaries or None: The retrieved data as a list of dictionaries, where each dictionary represents a row of data with the following keys:
            - "time" (str): The formatted timestamp of the data in the format "%Y-%m-%d %H:%M:%S".
            - "Compliant" (int): The amount of compliant data.
            - "NonCompliant" (int): The amount of non-compliant data.
            The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'time': '2024-02-29 12:30:45', 'Compliant': 10, 'NonCompliant': 5}, {'time': '2024-02-29 08:15:20', 'Compliant': 5, 'NonCompliant': 2}]
    """

    def get_today_data(self, cursor):
        try:

            current_datetime_utc = datetime.utcnow()
            offset_timedelta = timedelta(hours=3)

            local_start_of_day = current_datetime_utc + offset_timedelta
            local_start_of_day = local_start_of_day.replace(
                hour=0, minute=0, second=0, microsecond=0)
            local_end_of_day = local_start_of_day + timedelta(days=1)

            sql_query = """ 
                SELECT * 
                FROM Uniform 
                WHERE Timestamp >= ? AND Timestamp < ? 
            """

            cursor.execute(sql_query, (local_start_of_day, local_end_of_day))
            rows = cursor.fetchall()

            data = []
            for row in rows:
                timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                compliance = {
                    "Compliant": 0,
                    "NonCompliant": 0,
                }
                compliance[row[1]] = row[2]
                data.append({"time": timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"), **compliance})
            return data

        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False

    """
    Retrieves data for the current week from the "Uniform" table in the database.

    Args:
        cursor (database cursor): The database cursor object used for executing SQL queries.

    Returns:
        list of dictionaries or None: The retrieved data as a list of dictionaries, where each dictionary represents a row of data with the following keys:
            - "time" (str): The formatted timestamp of the data in the format "%Y-%m-%d %H:%M:%S".
            - "Compliant" (int): The amount of compliant data.
            - "NonCompliant" (int): The amount of non-compliant data.
            The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'time': '2024-02-25 12:30:45', 'Compliant': 10, 'NonCompliant': 5}, {'time': '2024-02-26 08:15:20', 'Compliant': 5, 'NonCompliant': 2}]
    """

    def get_week_data(self, cursor):
        try:
            current_date = datetime.now().date()
            last_sunday = current_date - \
                timedelta(days=(current_date.weekday()+1 % 7))
            current_saturday = last_sunday + timedelta(days=7)
            data = []

            sql_query = """ 
            SELECT * 
            FROM Uniform 
            WHERE Timestamp BETWEEN ? AND ? 
            """
            cursor.execute(
                sql_query, (str(last_sunday), str(current_saturday)))
            rows = cursor.fetchall()

            for row in rows:
                timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                compliance = {
                    "Compliant": 0,
                    "NonCompliant": 0,
                }
                compliance[row[1]] = row[2]
                data.append({"time": timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"), **compliance})

            return data

        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False

    def set_uniform_data(self, timestamp, uniform_type, amount, camera_id):
        try:

            conn = sqlite3.connect('monitoring-and-evaluation.db')
            cr = conn.cursor()

            self.__uniform_obj.Timestamp = timestamp
            self.__uniform_obj.Type = uniform_type
            self.__uniform_obj.Amount = amount
            self.__uniform_obj.Camera_ID = camera_id

            sql_query = """ 
                    INSERT INTO Uniform (Timestamp, Compliance, Amount, Camera_ID)
                    VALUES (?, ?, ?, ?);
                """
            cr.execute(sql_query, (self.__uniform_obj.Timestamp, self.__uniform_obj.Type,
                       self.__uniform_obj.Amount, self.__uniform_obj.Camera_ID))
            conn.commit()

        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False
