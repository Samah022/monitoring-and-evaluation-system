from .emotion import EmotionSate
from datetime import datetime, timedelta
from ..evaluationCriteriaManagement.emotionEntity import Emotion
import sqlite3


class EmotionDB:
    def __init__(self):
        self.__emotion_obj = Emotion()

    """
    Retrieves the current emotion data from the database.

    Args:
        cursor: The database cursor object.

    Returns:
        list of dictionaries or None: The retrieved emotion data as a list of dictionaries, where each dictionary represents a row of data with the following keys:
            - "label" (str): The emotion label.
            - "value" (int): The total amount of the emotion.
        The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'label': 'Happy', 'value': 10},
        {'label': 'Sad', 'value': 5},
        {'label': 'Neutral', 'value': 2}]
    """

    def get_current_data(self, cursor):
        try:
            data = []

            sql_query = """
            SELECT Type, SUM(Amount) AS TotalAmount 
            FROM Emotion 
            WHERE strftime('%H:%M', Timestamp) = strftime('%H:%M', datetime('now', 'localtime'))
            GROUP BY Type;
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
    Retrieves emotion data for the current year from the database.

    Args:
        cursor: The database cursor object.

    Returns:
        list of dictionaries or None: The retrieved emotion data as a list of dictionaries, where each dictionary represents a row of data with the following keys:
            - "time" (str): The timestamp of the emotion data in the format "YYYY-MM-DD HH:MM:SS".
            - "Happy" (int): The amount of happy emotions.
            - "Surprise" (int): The amount of surprise emotions.
            - "Neutral" (int): The amount of neutral emotions.
            - "Sad" (int): The amount of sad emotions.
            - "Angry" (int): The amount of angry emotions.
            - "Disgust" (int): The amount of disgust emotions.
        The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'time': '2022-01-01 08:30:00', 'Happy': 10, 'Surprise': 5, 'Neutral': 2, 'Sad': 3, 'Angry': 1, 'Disgust': 0},
        {'time': '2022-02-02 09:45:00', 'Happy': 8, 'Surprise': 4, 'Neutral': 0, 'Sad': 2, 'Angry': 3, 'Disgust': 1}]
    """

    def get_month_data(self, cursor):
        try:
            current_year = datetime.now().year
            data = []

            sql_query = """ 
                SELECT * 
                FROM Emotion 
                WHERE Timestamp BETWEEN ? AND ?; 
            """
            start_of_year = f"{current_year}-01-01 00:00:00"
            end_of_year = f"{current_year}-12-31 23:59:59"

            cursor.execute(sql_query, (start_of_year, end_of_year))
            rows = cursor.fetchall()

            for row in rows:
                timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                happy_amount = 0
                surprise_amount = 0
                neutral_amount = 0
                sad_amount = 0
                angry_amount = 0
                disgust_amount = 0

                if row[1] == EmotionSate.HAPPY.value:
                    happy_amount = row[2]
                elif row[1] == EmotionSate.SURPRISE.value:
                    surprise_amount = row[2]
                elif row[1] == EmotionSate.NEUTRAL.value:
                    neutral_amount = row[2]
                elif row[1] == EmotionSate.SAD.value:
                    sad_amount = row[2]
                elif row[1] == EmotionSate.ANGRY.value:
                    angry_amount = row[2]
                elif row[1] == EmotionSate.DISGUST.value:
                    disgust_amount = row[2]

                data.append({
                    "time": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    EmotionSate.HAPPY.value: happy_amount,
                    EmotionSate.SURPRISE.value: surprise_amount,
                    EmotionSate.NEUTRAL.value: neutral_amount,
                    EmotionSate.SAD.value: sad_amount,
                    EmotionSate.ANGRY.value: angry_amount,
                    EmotionSate.DISGUST.value: disgust_amount
                })

            return data

        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False

    """
    Retrieves emotion data for the current day from the database.

    Args:
        cursor: The database cursor object.

    Returns:
        list of dictionaries or None: The retrieved emotion data as a list of dictionaries, where each dictionary represents a row of data with the following keys:
            - "time" (str): The timestamp of the emotion data in the format "YYYY-MM-DD HH:MM:SS".
            - "Happy" (int): The amount of happy emotions.
            - "Surprise" (int): The amount of surprise emotions.
            - "Neutral" (int): The amount of neutral emotions.
            - "Sad" (int): The amount of sad emotions.
            - "Angry" (int): The amount of angry emotions.
            - "Disgust" (int): The amount of disgust emotions.
        The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'time': '2022-02-29 08:30:00', 'Happy': 10, 'Surprise': 5, 'Neutral': 2, 'Sad': 3, 'Angry': 1, 'Disgust': 0},
        {'time': '2022-02-29 09:45:00', 'Happy': 8, 'Surprise': 4, 'Neutral': 0, 'Sad': 2, 'Angry': 3, 'Disgust': 1}]
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
                FROM Emotion
                WHERE Timestamp >= ? AND Timestamp < ?
            """

            cursor.execute(sql_query, (local_start_of_day, local_end_of_day))
            rows = cursor.fetchall()

            data = []
            for row in rows:
                timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                emotions = {
                    EmotionSate.HAPPY.value: 0,
                    EmotionSate.SURPRISE.value: 0,
                    EmotionSate.NEUTRAL.value: 0,
                    EmotionSate.SAD.value: 0,
                    EmotionSate.ANGRY.value: 0,
                    EmotionSate.DISGUST.value: 0
                }
                emotions[row[1]] = row[2]
                data.append({"time": timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"), **emotions})
            return data

        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False

    """
    Retrieves emotion data for the current week from the database.

    Args:
        cursor: The database cursor object.

    Returns:
        list of dictionaries or None: The retrieved emotion data as a list of dictionaries, where each dictionary represents a row of data with the following keys:
            - "time" (str): The timestamp of the emotion data in the format "YYYY-MM-DD HH:MM:SS".
            - "Happy" (int): The amount of happy emotions.
            - "Surprise" (int): The amount of surprise emotions.
            - "Neutral" (int): The amount of neutral emotions.
            - "Sad" (int): The amount of sad emotions.
            - "Angry" (int): The amount of angry emotions.
            - "Disgust" (int): The amount of disgust emotions.
        The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'time': '2022-02-27 08:30:00', 'Happy': 10, 'Surprise': 5, 'Neutral': 2, 'Sad': 3, 'Angry': 1, 'Disgust': 0},
        {'time': '2022-02-28 09:45:00', 'Happy': 8, 'Surprise': 4, 'Neutral': 0, 'Sad': 2, 'Angry': 3, 'Disgust': 1}]
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
                    FROM Emotion 
                    WHERE Timestamp BETWEEN ? AND ? 
                """
            cursor.execute(
                sql_query, (str(last_sunday), str(current_saturday)))
            rows = cursor.fetchall()

            for row in rows:
                timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                emotions = {
                    EmotionSate.HAPPY.value: 0,
                    EmotionSate.SURPRISE.value: 0,
                    EmotionSate.NEUTRAL.value: 0,
                    EmotionSate.SAD.value: 0,
                    EmotionSate.ANGRY.value: 0,
                    EmotionSate.DISGUST.value: 0
                }
                emotions[row[1]] = row[2]
                data.append({"time": timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"), **emotions})

            return data
        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False

    def set_emotion_data(self, timestamp, emotion_type, amount, camera_id):
        try:

            conn = sqlite3.connect('monitoring-and-evaluation.db')
            cr = conn.cursor()

            self.__emotion_obj.Timestamp = timestamp
            self.__emotion_obj.Type = emotion_type
            self.__emotion_obj.Amount = amount
            self.__emotion_obj.Camera_ID = camera_id

            sql_query = """ 
                    INSERT INTO Emotion (Timestamp, Type, Amount, Camera_ID)
                    VALUES (?, ?, ?, ?);
                """
            cr.execute(sql_query, (self.__emotion_obj.Timestamp, self.__emotion_obj.Type,
                       self.__emotion_obj.Amount, self.__emotion_obj.Camera_ID))
            conn.commit()

        except Exception as e:
            print("Error connecting to database or retrieving data: ", e)
            return False
