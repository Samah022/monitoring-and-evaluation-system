from abc import ABC, abstractmethod
from ...servicesHandler.servicesHandler import ServicesHandler


class DetectionModelAdaptor(ABC):
    def __init__(self):
        self.services_handler = ServicesHandler()
    """
    Abstract method to predict using the detection model.

    Args:
        camera_url (str): The URL of the camera feed.

    Returns:
        None
    """
    @abstractmethod
    def predict(self, camera_link):
        pass
