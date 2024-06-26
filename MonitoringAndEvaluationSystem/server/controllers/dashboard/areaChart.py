from .chart import Chart


class AreaChart(Chart):

    """
    Updates the data for an area chart.

    Args:
        data (dict): The data to be updated for the area chart.

    Returns:
        dict: A dictionary containing the updated data for the area chart, with the following keys:
            - "type" (str): The type of the area chart, which is dynamically set based on the instance's name.
            - "data" (dict): The updated data for the area chart.
    """

    async def update(self, data):
        result = {
            "type": f"{self.name}_areachart",
            "data": data,
        }
        return result
