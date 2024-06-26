from abc import ABC, abstractmethod


class Chart (ABC):

    def __init__(self, name):
        self.name = name

    """
    Abstract method to update the chart with new data.

    Args:
        data: The data to update the chart with.

    Returns:
        dict: A dictionary containing the updated data for the chart. The structure of the dictionary
            should be specified in subclasses.
    """
    @abstractmethod
    def update(self, data):
        pass
