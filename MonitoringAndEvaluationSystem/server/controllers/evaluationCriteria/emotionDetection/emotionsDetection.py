import time
import threading
from datetime import datetime
from collections import defaultdict
from ..emotionModel.emotionModel import EmotionModel
from ..criteriaDetectionBehavior.detectionBehavior import DetectionBehavior


class EmotionsDetection(DetectionBehavior):
    def __init__(self):
        super().__init__()
        self.__emotion_predictor = EmotionModel()

    """
    Perform emotion detection on frames from the specified camera.

    Args:
        camera_ID (str): The ID of the camera.
        camera_link (str): The URL of the camera feed.

    Returns:
        None
    """

    def detect(self, cameraID, camera_link):
        prediction_thread = threading.Thread(
            target=self.__emotion_predictor.predict, args=(camera_link,))
        results_thread = threading.Thread(
            target=self.__save_result, args=(cameraID,))

        prediction_thread.start()
        results_thread.start()

        prediction_thread.join()
        results_thread.join()

    """
    Process the results of emotion detection for frames from a camera.

    Args:
        cameraID (str): The ID of the camera.

    Returns:
        None
    """

    def __save_result(self, cameraID):
        waiting_time = 30
        frames_result = []
        combined_result = []
        DB_result = []

        while True:
            emotion_prediction_result = self.__emotion_predictor.get_emotion_results()
            if emotion_prediction_result:
                face_id, emotion_result, emotion_score = emotion_prediction_result.pop(0)
                frames_result.append(
                    {"id": face_id, "type": emotion_result, "score": emotion_score})

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            min_no_of_frame = 70
            grouped_results = {}
            if len(frames_result) > min_no_of_frame:
                for frame_result in frames_result:
                    id = frame_result["id"]
                    if id not in grouped_results:
                        grouped_results[id] = []
                    grouped_results[id].append(frame_result)

                frame_result = []
                
                threshold_score = 0.7 #0.6
                for id, results in grouped_results.items():
                    emotion , score = self.guess_possible_result(results)
                    print("guess possible result", emotion, score)
                    if score > threshold_score:
                        combined_result.append({"id": id, "emotion": emotion})

                grouped_results = {}

                emotion_count = []
                for entry in combined_result:
                    emotion = entry["emotion"]
                    found = False
                    for item in emotion_count:
                        if item["emotion"] == emotion:
                            item["amount"] += 1
                            found = True
                            break
                    if not found:
                        emotion_count.append({"emotion": emotion, "amount": 1})

                combined_result = []

                for entry in emotion_count:
                    emotion = entry["emotion"]
                    amount = entry["amount"]
                    DB_result.append(
                        {"cameraID": cameraID, "emotion": emotion, "amount": amount, "time": current_time})

                emotion_count = []

                for result in DB_result:
                    self.db_facade.set_emotion_data(
                        result["time"], result["emotion"], result["amount"], result["cameraID"])
                print("result in DB", DB_result)
                DB_result = []

                frames_result = []
                time.sleep(waiting_time)
