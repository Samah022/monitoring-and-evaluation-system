from abc import ABC, abstractmethod
from ...models.DBManagement.DBFacade import DBFacade


class DataManager(ABC):
    def __init__(self):
        self.chart_list = []
        self.db = DBFacade()

    """
    Add a chart to the list of registered charts.

    Args:
        chart: The chart object to be added.

    Returns:
        bool: True if the chart is added successfully, False otherwise.
    """

    def add_chart(self, chart):
        try:
            self.chart_list.append(chart)
            return True
        except Exception as e:
            print(f"An error occurred while adding chart: {e}")
            return False

    """
    Abstract method to notify all registered charts.

    Returns:
        list: A list containing the results of updating all charts. Each result is a dictionary
            containing the updated data for a chart.
    """
    @abstractmethod
    def notify_all(self):
        pass

    """
    Abstract method to set data and notify all registered charts.

    Returns:
        list: A list containing the results of updating all charts. Each result is a dictionary
            containing the updated data for a chart.
    """
    @abstractmethod
    def set_data(self):
        pass
