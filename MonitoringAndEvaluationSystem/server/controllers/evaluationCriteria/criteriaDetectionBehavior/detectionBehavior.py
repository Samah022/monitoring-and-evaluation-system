from collections import defaultdict
from ....models.DBManagement.DBFacade import DBFacade


class DetectionBehavior:
    def __init__(self):
        self.db_facade = DBFacade()
        self.model = None

    """
    Perform detection using the assigned model on frames from the specified camera.

    Args:
        camera_ID (str): The ID of the camera.
        camera_url (str): The URL of the camera feed.

    Returns:
        None

    """

    def detect(self, camera_ID, camera_url):
        pass

    """
    Guess the most probable emotion from a list of emotion detection results with weights.

    Args:
        prediction_results (list): A list of dictionaries containing emotion detection results with 'emotion' and 'score' keys.

    Returns:
        str or None: The most probable emotion, or None if no emotion results are available.
    """

    def guess_possible_result(self, prediction_results):
        criteria_stats = defaultdict(lambda: {'total_score': 0, 'count': 0})

        for result in prediction_results:
            type = result['type']
            score = result['score']
            if type is not None and score is not None:
                criteria_stats[type]['total_score'] += score
                criteria_stats[type]['count'] += 1

        weighted_criteria = {}
        for type, stats in criteria_stats.items():
            if stats['count'] > 0:
                weighted_score = stats['total_score'] / stats['count']
                weighted_criteria[type] = weighted_score

        guessed_criteria_type = max(
            weighted_criteria, key=weighted_criteria.get) if weighted_criteria else None

        guessed_criteria_score = weighted_criteria[guessed_criteria_type] if guessed_criteria_type else None
        return guessed_criteria_type, guessed_criteria_score
