from .criteria import Criteria
from .dressCodeDetection.uniformDetection import UniformDetection
from .emotionDetection.emotionsDetection import EmotionsDetection


class CriteriaFactory:
    """
        Create a criteria object based on the given criteria name.

        Args:
            criteriaName (str): The name of the criteria.

        Returns:
            object: An instance of the criteria object based on the given criteria name.
    """

    def create_criteria(self, criteria_name):
        if criteria_name == Criteria.EMOTION.value:
            return EmotionsDetection()

        elif criteria_name == Criteria.UNIFORM.value:
            return UniformDetection()
