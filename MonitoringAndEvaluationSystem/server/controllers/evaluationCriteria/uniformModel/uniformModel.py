import threading
from ..detectionModelAdaptor.detectionModelAdaptor import DetectionModelAdaptor


class UniformModel(DetectionModelAdaptor):

    def __init__(self):
        super().__init__()
        self.__uniform_results = []

    """
    Retrieve the custom uniform prediction results.

    Returns:
        A list of tuples containing the frame ID, uniform result, and uniform score.
    """

    def get_uniform_results(self):
        return self.__uniform_results

    """
        Perform uniform prediction on the specified camera URL.

        Args:
            camera_link (str): The URL of the camera feed.

        Returns:
            None
    """

    def predict(self, camera_link):
        prediction_thread = threading.Thread(
            target=self.services_handler.handle_uniform_predict, args=(camera_link,))
        results_thread = threading.Thread(target=self.set_uniform_results)

        prediction_thread.start()
        results_thread.start()

        prediction_thread.join()
        results_thread.join()

    """
        Process the custom uniform prediction results.

        Returns:
            None
    """

    def set_uniform_results(self):
        while True:
            prediction_result = self.services_handler.get_prediction_result()
            if prediction_result:
                frame_id, uniform_result, uniform_score = prediction_result.pop(0)
                self.__uniform_results.append(
                    (frame_id, uniform_result, uniform_score))
