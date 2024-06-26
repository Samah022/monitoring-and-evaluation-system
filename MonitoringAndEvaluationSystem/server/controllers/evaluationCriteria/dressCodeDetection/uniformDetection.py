from ..criteriaDetectionBehavior.detectionBehavior import DetectionBehavior
from ..uniformModel.uniformModel import UniformModel
from collections import defaultdict
from datetime import datetime
import threading
import time


class UniformDetection(DetectionBehavior):
    def __init__(self):
        super().__init__()
        self.__uniform_predictor = UniformModel()

    """
    Perform uniform detection on frames from the specified camera.

    Args:
        camera_ID (str): The ID of the camera.
        camera_link (str): The URL of the camera feed.

    Returns:
        None
    """

    def detect(self, cameraID, camera_link):
        prediction_thread = threading.Thread(
            target=self.__uniform_predictor.predict, args=(camera_link,))
        results_thread = threading.Thread(
            target=self.__save_result, args=(cameraID,))

        prediction_thread.start()
        results_thread.start()

        prediction_thread.join()
        results_thread.join()

    """
    Process the results of uniform detection for frames from a camera.

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
            uniform_prediction_result = self.__uniform_predictor.get_uniform_results()
            if uniform_prediction_result:
                frame_id, uniform_result, uniform_score = uniform_prediction_result.pop(0)
                frames_result.append(
                    {"id": frame_id, "type": uniform_result, "score": uniform_score})

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            min_no_of_frame_results = 60
            grouped_results = {}
            if len(frames_result) > min_no_of_frame_results:
                for frame_result in frames_result:
                    id = frame_result["id"]
                    if id not in grouped_results:
                        grouped_results[id] = []
                    grouped_results[id].append(frame_result)

                frame_result = []
                
                threshold_score=0.6
                for id, results in grouped_results.items():
                    uniform, score = self.guess_possible_result(results)
                    print("guess possible result", uniform, score)
                    if score >= threshold_score:
                        combined_result.append({"id": id, "uniform": uniform})

                grouped_results = {}

                uniform_count = []
                for entry in combined_result:
                    uniform = entry["uniform"]
                    found = False
                    for item in uniform_count:
                        if item["uniform"] == uniform:
                            item["amount"] += 1
                            found = True
                            break
                    if not found:
                        uniform_count.append({"uniform": uniform, "amount": 1})

                combined_result = []

                for entry in uniform_count:
                    uniform = entry["uniform"]
                    amount = entry["amount"]
                    DB_result.append({"cameraID": cameraID, "uniform": uniform,
                                      "amount": amount, "time": current_time})

                uniform_count = []

                for result in DB_result:
                    if result["uniform"] == "apron":

                        result["uniform"] = "Compliant"
                    else:
                        result["uniform"] = "NonCompliant"

                    self.db_facade.set_uniform_data(
                        result["time"], result["uniform"], result["amount"], result["cameraID"])
                print("result in DB", DB_result)
                DB_result = []

                frames_result = []
                time.sleep(waiting_time)
