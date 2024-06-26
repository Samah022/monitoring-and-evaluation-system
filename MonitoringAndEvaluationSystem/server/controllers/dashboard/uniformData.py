from .pieChart import PieChart
from .areaChart import AreaChart
from .dataManager import DataManager


class UniformData(DataManager):
    def __init__(self):
        super().__init__()
        self.__uniform_current_data = []
        self.__uniform_month_data = []
        self.__uniform_today_data = []
        self.__uniform_week_data = []

    """
    Retrieves the uniform current data.

    Returns:
        list: A list of dictionaries containing the uniform current data. Each dictionary represents
              a data point with a label and a value, such as {'label': 'NonCompliant', 'value': 2}.
    """

    def get_uniform_current_data(self):
        return self.__uniform_current_data

    """
    Retrieves the uniform data for the month.

    Returns:
        list: A list of dictionaries containing the uniform data for the month. Each dictionary represents
              data for a specific time point within the current month, with keys for time and categories such as
              'Compliant' and 'NonCompliant'.
    """

    def get_uniform_month_data(self):
        return self.__uniform_month_data

    """
    Retrieves the uniform data for today.

    Returns:
        list: A list of dictionaries containing the uniform data for today. Each dictionary represents
              data for a specific time point within the current day, with keys for time and categories such as
              'Compliant' and 'NonCompliant'.
    """

    def get_uniform_today_data(self):
        return self.__uniform_today_data

    """
    Retrieves the uniform data for the week.

    Returns:
        list: A list of dictionaries containing the uniform data for the week. Each dictionary represents
              data for a specific time point within the week, with keys for time and categories such as
              'Compliant' and 'NonCompliant'.
    """

    def get_uniform_week_data(self):
        return self.__uniform_week_data

    """
    Notifies all registered charts with updated data.
    Iterates over each chart in the chart list and updates them with specific data based on their type.

    Returns:
        list: A list containing the results of updating all charts. Each result is a dictionary
              containing the updated data for a chart. For PieChart instances, the dictionary has the
              following keys:
              - "type" (str): The type of the chart.
              - "data" (dict): The updated data for the chart.
              For AreaChart instances, the dictionary has the following keys:
              - "type" (str): The type of the chart.
              - "data" (dict): The updated data for the chart, containing keys "months", "week", and "today".
              The list is empty if no data is found or False if an error occurs.

    Raises:
        Exception: If an error occurs while notifying all charts.
    """

    async def notify_all(self):
        all_results = []
        try:
            for chart in self.chart_list:
                if isinstance(chart, PieChart):
                    result = await chart.update(self.get_uniform_current_data())
                    all_results.append(result)
                elif isinstance(chart, AreaChart):
                    result = await chart.update({"months": self.get_uniform_month_data(), "week": self.get_uniform_week_data(), "today": self.get_uniform_today_data()})
                    all_results.append(result)
            return all_results
        except Exception as e:
            print(f"Error notifying all: {e}")
            return False

    """
    Sets uniform data for different timeframes and notifies all registered charts.

    Retrieves uniform current, month, today, and week data from the database and updates
    corresponding attributes. Then, notifies all registered charts with the updated data.
    For PieChart instances, updates with the current emotion data.
    For AreaChart instances, updates with data containing emotion data for the current month, week, and today.

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
            self.set_uniform_current_data()
            self.set_uniform_month_data()
            self.set_uniform_today_data()
            self.set_uniform_week_data()
            all_results = await self.notify_all()
            return all_results
        except Exception as e:
            print(f"Error setting data: {e}")
            return False

    """
    Sets the uniform current data from the database.

    Retrieves the uniform current data from the database and assigns it to the private attribute __uniform_current_data.

    Returns:
        None
    """

    def set_uniform_current_data(self):
        self.__uniform_current_data = self.db.get_uniform_current_data()

    """
    Sets the uniform month data from the database.

    Retrieves the uniform month data from the database and assigns it to the private attribute __uniform_month_data.

    Returns:
        None
    """

    def set_uniform_month_data(self):
        self.__uniform_month_data = self.db.get_uniform_month_data()

    """
    Sets the uniform today's data from the database.

    Retrieves the uniform today's data from the database and assigns it to the private attribute __uniform_today_data.

    Returns:
        None
    """

    def set_uniform_today_data(self):
        self.__uniform_today_data = self.db.get_uniform_today_data()

    """
    Sets the uniform week data from the database.

    Retrieves the uniform week data from the database and assigns it to the private attribute __uniform_week_data.

    Returns:
        None
    """

    def set_uniform_week_data(self):
        self.__uniform_week_data = self.db.get_uniform_week_data()
