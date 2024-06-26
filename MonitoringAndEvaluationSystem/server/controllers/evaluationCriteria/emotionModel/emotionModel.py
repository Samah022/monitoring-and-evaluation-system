import threading
from ..detectionModelAdaptor.detectionModelAdaptor import DetectionModelAdaptor


class EmotionModel(DetectionModelAdaptor):

    def __init__(self):
        super().__init__()
        self.__emotion_results = []

    """
    Retrieve the custom emotion prediction results.

    Returns:
        A list of tuples containing the frame ID, emotion result, and emotion score.
    """

    def get_emotion_results(self):
        return self.__emotion_results

    """
    Perform emotion prediction on the specified camera URL.

    Args:
        camera_link (str): The URL of the camera feed.

    Returns:
        None
    """

    def predict(self, camera_link):
        prediction_thread = threading.Thread(
            target=self.services_handler.handle_emotion_predict, args=(camera_link,))
        results_thread = threading.Thread(target=self.set_emotion_results)

        prediction_thread.start()
        results_thread.start()

        prediction_thread.join()
        results_thread.join()

    """
    Process the custom emotion prediction results.

    Returns:
        None
    """

    def set_emotion_results(self):
        while True:
            prediction_result = self.services_handler.get_prediction_result()
            if prediction_result:
                frame_id, emotion_result, emotion_score = prediction_result.pop(0)
                self.__emotion_results.append(
                    (frame_id, emotion_result, emotion_score))
