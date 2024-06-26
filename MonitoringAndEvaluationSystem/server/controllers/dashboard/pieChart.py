from .chart import Chart


class PieChart(Chart):
    """
    Updates the data for the pie chart.

    Args:
        data (dict): The updated data for the pie chart.

    Returns:
        dict: A dictionary containing the updated data for the pie chart, with the following keys:
            - "type" (str): The type of the pie chart, which is dynamically set based on the instance's name.
            - "data" (dict): The updated data for the pie chart.
    """

    async def update(self, data):
        result = {
            "type": f"{self.name}_piechart",
            "data": data,
        }
        return result
