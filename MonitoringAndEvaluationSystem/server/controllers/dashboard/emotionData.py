from .dataManager import DataManager
from .pieChart import PieChart
from .areaChart import AreaChart


class EmotionData(DataManager):
    def __init__(self):
        super().__init__()
        self.__emotion_current_data = []
        self.__emotion_month_data = []
        self.__emotion_today_data = []
        self.__emotion_week_data = []

    """
    Retrieves the current emotion data.

    Returns:
        list: A list of dictionaries containing the current emotion data. Each dictionary represents
              a data point with a label and a value, such as {'label': 'Sad', 'value': 3}.
    """

    def get_emotion_current_data(self):
        return self.__emotion_current_data

    """
    Retrieves the emotion data for the current month.

    Returns:
        list: A list of dictionaries containing the emotion data for the current month. Each dictionary represents
              data for a specific time point, with keys for time and emotional categories such as
              'Happy', 'Surprise', 'Neutral', 'Sad', 'Angry', and 'Disgust'.
    """

    def get_emotion_month_data(self):
        return self.__emotion_month_data

    """
    Retrieves the emotion data for today.

    Returns:
        list: A list of dictionaries containing the emotion data for today. Each dictionary represents
              data for a specific time point within the current day, with keys for time and emotional
              categories such as 'Happy', 'Surprise', 'Neutral', 'Sad', 'Angry', and 'Disgust'.
    """

    def get_emotion_today_data(self):
        return self.__emotion_today_data

    """
    Retrieves the emotion data for the current week.

    Returns:
        list: A list of dictionaries containing the emotion data for the current week. Each dictionary represents
              data for a specific time point within the current week, with keys for time and emotional categories such as
              'Happy', 'Surprise', 'Neutral', 'Sad', 'Angry', and 'Disgust'.
    """

    def get_emotion_week_data(self):
        return self.__emotion_week_data

    """
    Notifies all registered charts with updated emotion data.

    Iterates over each chart in the chart list and updates them with specific emotion data based on their type.
    For PieChart instances, updates with the current emotion data.
    For AreaChart instances, updates with data containing emotion data for the current month, week, and today.

    Returns:
        list: A list containing the results of updating all charts. Each result is a dictionary
              containing the updated data for a chart. For the structure of each dictionary, see the
              documentation of the `update` method.
              The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If an error occurs while notifying all charts.
    """

    async def notify_all(self):
        all_results = []
        try:
            for chart in self.chart_list:
                if isinstance(chart, PieChart):
                    result = await chart.update(self.get_emotion_current_data())
                    all_results.append(result)
                elif isinstance(chart, AreaChart):
                    result = await chart.update({"months": self.get_emotion_month_data(), "week": self.get_emotion_week_data(), "today": self.get_emotion_today_data()})
                    all_results.append(result)
            return all_results
        except Exception as e:
            print(f"Error notifying all: {e}")
            return False

    """
    Sets emotion data for different timeframes and notifies all registered charts.

    Retrieves emotion data for the current month, week, today, and current data from the database
    and updates corresponding attributes. Then, notifies all registered charts with the updated data.

    Returns:
        list: A list containing the results of updating all charts. Each result is a dictionary
              containing the updated data for a chart. For the structure of each dictionary, see the
              documentation of the `notify_all` method.
              The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If an error occurs while setting data or notifying all charts.
    """

    async def set_data(self):
        try:
            self.set_emotion_current_data()
            self.set_emotion_month_data()
            self.set_emotion_today_data()
            self.set_emotion_week_data()
            all_results = await self.notify_all()
            return all_results
        except Exception as e:
            print(f"Error setting data: {e}")
            return False

    """
    Sets the emotion data for the current period.

    Retrieves the emotion data for the current period from the database and assigns it to the private attribute __emotion_current_data.

    Returns:
        None
    """

    def set_emotion_current_data(self):
        self.__emotion_current_data = self.db.get_emotion_current_data()

    """
    Sets the emotion data for the current month.

    Retrieves the emotion data for the current month from the database and assigns it to the private attribute __emotion_month_data.

    Returns:
        None
    """

    def set_emotion_month_data(self):
        self.__emotion_month_data = self.db.get_emotion_month_data()

    """
    Sets the emotion data for today.

    Retrieves the emotion data for today from the database and assigns it to the private attribute __emotion_today_data.

    Returns:
        None
    """

    def set_emotion_today_data(self):
        self.__emotion_today_data = self.db.get_emotion_today_data()

    """
    Sets the emotion data for the current week.

    Retrieves the emotion data for the current week from the database and assigns it to the private attribute __emotion_week_data.

    Returns:
        None
    """

    def set_emotion_week_data(self):
        self.__emotion_week_data = self.db.get_emotion_week_data()
