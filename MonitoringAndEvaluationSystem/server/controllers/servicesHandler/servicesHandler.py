import asyncio
from ..user.user import User
from inference import InferencePipeline
from ..dashboard.pieChart import PieChart
from ..dashboard.areaChart import AreaChart
from ..camera.cameraBoard import CameraBoard
from ..dashboard.emotionData import EmotionData
from ..dashboard.uniformData import UniformData
from inference.core.interfaces.camera.entities import VideoFrame


class ServicesHandler:

    def __init__(self):
        self.__camera_board = CameraBoard()
        self.__connected_user = User("", "")
        self.__subject_emotion = EmotionData()
        self.__subject_uniform = UniformData()
        self.__prediction_results = []

    """
    Retrieve the prediction results.

    Returns:
        dict: The prediction results stored.
    """

    def get_prediction_result(self):
        return self.__prediction_results

    """
    Handles adding a new camera to the system.

    Args:
        new_camera (Camera): The new camera object to be added.

    Returns:
        dict: A dictionary indicating whether the camera was successfully added or not.
    """

    def handle_add_camera(self, new_camera):
        if self.__camera_board.add_camera(new_camera):
            return {"state": True}
        return {"state": False}

    """
    Retrieving the connected user.

    Returns:
        User: The user object representing the connected user.
    """

    def handle_connected_user(self):
        return self.__connected_user

    """
        Handle emotion prediction for a given camera URL using an emotion detection model.

        Args:
            camera_url (str): The URL of the camera feed.

        Returns:
            None
    """

    def handle_emotion_predict(self, camera_link):
        pipeline = InferencePipeline.init(
            model_id="emotion-detection-cwq4g/1",
            api_key="CL44RJt0AHwiczZPxMLN",
            video_reference=camera_link,
            on_prediction=lambda predictions, video_frame: self.set_prediction_result(
                predictions, video_frame),
        )
        pipeline.start()
        pipeline.join()

    """
    Handles fetching data for the dashboard asynchronously.

    Yield:
        chart_data : updated data for the dashboard charts.
    """

    async def handle_fetch_dashboard_data(self):
        uniform_pie = PieChart("uniform")
        emotion_pie = PieChart("emotion")
        uniform_area = AreaChart("uniform")
        emotion_area = AreaChart("emotion")

        self.__subject_emotion .add_chart(emotion_area)
        self.__subject_emotion .add_chart(emotion_pie)

        self.__subject_uniform .add_chart(uniform_area)
        self.__subject_uniform .add_chart(uniform_pie)

        data_list = [self.__subject_emotion, self.__subject_uniform]

        tasks = [
            asyncio.create_task(data.set_data())
            for data in data_list
        ]
        results = await asyncio.gather(*tasks)
        for criteria in results:
            if (criteria != False):
                for chart_data in criteria:
                    yield chart_data

    """
    Handles retrieving information about all cameras in the system.

    Returns:
        dict: A dictionary containing information about all cameras. 
              The keys represent the camera IDs, and the values contain 
              details about each camera, such as its name, link, and criteria.
    """

    def handle_get_all_cameras(self):
        result = self.__camera_board.get_all_cameras()
        return {"data": result}

    """
    Handles starting the streaming of video frames from connected cameras.

    Args:
        connected_cameras (dict): A dictionary containing information about connected cameras. 
                                  The keys represent the camera IDs, and the values contain 
                                  the camera links.
        websocket: The websocket connection for streaming frames.

    Returns:
        None
    """

    async def handle_start_streaming(self, connected_cameras, websocket):
        async def send_frames_from_camera(camera_id, websocket):
            async for frame_data in self.__camera_board.start_streaming(camera_id, connected_cameras):
                await websocket.send_json(frame_data)

        tasks = [send_frames_from_camera(
            camera_id, websocket) for camera_id in connected_cameras.keys()]
        await asyncio.gather(*tasks)

    """
        Handle uniform prediction for a given camera URL using an uniform detection model.

        Args:
            camera_url (str): The URL of the camera feed.

        Returns:
            None
    """

    def handle_uniform_predict(self, camera_url):
        pipeline = InferencePipeline.init(
            model_id="kv_ap_03/1",
            api_key="CL44RJt0AHwiczZPxMLN",
            video_reference=camera_url,
            on_prediction=lambda predictions, video_frame: self.set_prediction_result(
                predictions, video_frame),
        )
        pipeline.start()
        pipeline.join()

    """
        This method takes the predictions from the detection model and extracts the 
        labels and confidence scores. It then iterates over each label-confidence pair, assigns a 
        unique frame ID, and appends the frame ID, label, and confidence score as a tuple 
        to the `results` list attribute of the ServicesHandler instance. 

        Args:
            predictions (dict): A dictionary containing the model predictions from the model.
            video_frame (VideoFrame): The video frame associated with the predictions.

        Returns:
            None
    """

    def set_prediction_result(self, predictions: dict, video_frame: VideoFrame):

        labels_confidence = [(p["class"], p["confidence"])
                             for p in predictions["predictions"]]
        if labels_confidence:
            for id, label_confidence in enumerate(labels_confidence):
                prediction_result = label_confidence[0]
                prediction_score = label_confidence[1]
                frame_id = id
                self.__prediction_results.append(
                    (frame_id, prediction_result, prediction_score))
