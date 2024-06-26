# Local
from ...db_connect import cr
from .emotion import EmotionSate
from .cameraDB import CameraDB
from .emotionDB import EmotionDB
from .uniformDB import UniformDB


class DBFacade:

    def __init__(self):
        self.__cameraDB = CameraDB()
        self.__emotiondb = EmotionDB()
        self.__uniformdb = UniformDB()

        """
        Adds a camera to the database.

        Args:
            name (str): The name of the camera to be added.
            link (str): The URL or link of the camera.
            criteria (list of str): The evaluation criteria for the camera.

        Returns:
            bool: True if the camera is successfully added, False otherwise.
        """

    def add_camera(self, name: str, link: str, criteria: list) -> bool:
        return self.__cameraDB.add_camera(name, link, criteria)

    """
    Retrieves information about all cameras from the database.

    Returns:
        list of dictionaries or None: The retrieved camera information as a list of dictionaries {id, name, link, criteria}.
        Return empty list if no cameras are found or None if an error occurs.
    """

    def get_all_cameras(self):
        return self.__cameraDB.get_all_cameras()

    """
    Retrieves the current emotion data from the emotion database.

    Returns:
        list of dictionaries or None: Return the current emotion data as a dictionary {label, value}. 
        Returns None if no current emotion data is available or if an error occurs.
    """

    def get_emotion_current_data(self):
        return self.__emotiondb.get_current_data(cr)

    """
    Retrieves the emotion data for the current month from the emotion database and combined the data in same day.

    Returns:
        list of dictionaries or None: The emotion data for the current month as a list of dictionaries {time, Happy, Surprise, Neutral, Sad, Angry, Disgust}.
        Return empty list if no data is found or None if an error occurs.
    """

    def get_emotion_month_data(self):
        data = self.__emotiondb.get_month_data(cr)
        combined_data = {}
        for item in data:
            timestamp = item['time']
            if timestamp not in combined_data:
                combined_data[timestamp] = item
            else:
                for emotion in [EmotionSate.HAPPY.value, EmotionSate.SURPRISE.value, EmotionSate.NEUTRAL.value, EmotionSate.SAD.value, EmotionSate.ANGRY.value, EmotionSate.DISGUST.value]:
                    combined_data[timestamp][emotion] += item[emotion]
        result = list(combined_data.values())
        return result

    """
    Retrieves the emotion data for the current day from the emotion database and combined the data in same day.

    Returns:
        list of dictionaries or None: The emotion data for the current day as a list of dictionaries {time, Happy, Surprise, Neutral, Sad, Angry, Disgust}. 
        Return empty list if no data is found or None if an error occurs.
    """

    def get_emotion_today_data(self):
        data = self.__emotiondb.get_today_data(cr)
        combined_data = {}
        for item in data:
            timestamp = item['time']
            if timestamp not in combined_data:
                combined_data[timestamp] = item
            else:
                for emotion in [EmotionSate.HAPPY.value, EmotionSate.SURPRISE.value, EmotionSate.NEUTRAL.value, EmotionSate.SAD.value, EmotionSate.ANGRY.value, EmotionSate.DISGUST.value]:
                    combined_data[timestamp][emotion] += item[emotion]
        result = list(combined_data.values())
        return result

    """
    Retrieves the emotion data for the current week from the emotion database and combined the data in same day.

    Returns:
        list of dictionaries or None: The emotion data for the current week as a list of dictionaries {time, Happy, Surprise, Neutral, Sad, Angry, Disgust}. 
        Return empty list if no data is found or None if an error occurs.
    """

    def get_emotion_week_data(self):
        data = self.__emotiondb.get_week_data(cr)
        combined_data = {}
        for item in data:
            timestamp = item['time']
            if timestamp not in combined_data:
                combined_data[timestamp] = item
            else:
                for emotion in [EmotionSate.HAPPY.value, EmotionSate.SURPRISE.value, EmotionSate.NEUTRAL.value, EmotionSate.SAD.value, EmotionSate.ANGRY.value, EmotionSate.DISGUST.value]:
                    combined_data[timestamp][emotion] += item[emotion]
        result = list(combined_data.values())
        return result

    """
    Retrieves the current uniform data from the uniform database.

    Returns:
        list of dictionaries or None: The current uniform data as a dictionary {label, value}.
        Returns empty list if no data is found or None if an error occurs.
    """

    def get_uniform_current_data(self):
        return self.__uniformdb.get_current_data(cr)

    """
    Retrieves the uniform data for the current month from the uniform database and combined the data in same day.

    Returns:
        list of dictionaries or None: The uniform data for the current month as a list of dictionaries {time, Compliant, NonCompliant}.
        Return empty list if no data is found or None if an error occurs.
    """

    def get_uniform_month_data(self):
        data = self.__uniformdb.get_month_data(cr)
        combined_data = {}
        for item in data:
            timestamp = item['time']
            if timestamp not in combined_data:
                combined_data[timestamp] = item
            else:
                for compliance in ['Compliant', 'NonCompliant']:
                    combined_data[timestamp][compliance] += item[compliance]
        result = list(combined_data.values())
        return result

    """
    Retrieves the uniform data for the current day from the uniform database and combined the data in same day.

    Returns:
        list of dictionaries or None: The uniform data for the current day as a list of dictionaries {time, Compliant, NonCompliant}. 
        Return empty list if no data is found or None if an error occurs.
    """

    def get_uniform_today_data(self):
        data = self.__uniformdb.get_today_data(cr)
        combined_data = {}
        for item in data:
            timestamp = item['time']
            if timestamp not in combined_data:
                combined_data[timestamp] = item
            else:
                for compliance in ['Compliant', 'NonCompliant']:
                    combined_data[timestamp][compliance] += item[compliance]
        result = list(combined_data.values())
        return result

    """
    Retrieves the uniform data for the current week from the uniform database and combined the data in same day.

    Returns:
        list of dictionaries or None: The uniform data for the current week as a list of dictionaries {time, Compliant, NonCompliant}. 
        Return empty list if no data is found or None if an error occurs.
    """

    def get_uniform_week_data(self):
        data = self.__uniformdb.get_week_data(cr)
        combined_data = {}
        for item in data:
            timestamp = item['time']
            if timestamp not in combined_data:
                combined_data[timestamp] = item
            else:
                for compliance in ['Compliant', 'NonCompliant']:
                    combined_data[timestamp][compliance] += item[compliance]
        result = list(combined_data.values())
        return result

    def set_emotion_data(self, timestamp, emotion_type, amount, camera_id):
        self.__emotiondb.set_emotion_data(timestamp, emotion_type, amount, camera_id)

    def set_uniform_data(self, timestamp, uniform_type, amount, camera_id):
        self.__uniformdb.set_uniform_data(timestamp, uniform_type, amount, camera_id)
