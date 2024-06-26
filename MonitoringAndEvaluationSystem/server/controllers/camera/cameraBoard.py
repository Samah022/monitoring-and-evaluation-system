# from .camera import Camera
from ...models.DBManagement.DBFacade import DBFacade


class CameraBoard:
    def __init__(self):
        self.__camera_list = []
        self.__DBFacade = DBFacade()

    """
    Adds a camera to the system.

    Args:
        camera (Camera): The camera object to be added.
    
    Raises:
        TypeError: If the camera is not a Camera Object.

    Returns:
        bool: True if the camera is successfully added, False otherwise.
    """

    def add_camera(self, camera):
        from .camera import Camera
        try:
            if not isinstance(camera, Camera) and camera is not None:
                raise TypeError("Invalid camera. Expected Camera Object.")

            if self.__DBFacade.add_camera(camera.get_camera_name(), camera.get_camera_URL(), camera.get_evaluation_criteria()):
                return True
            else:
                return False

        except Exception as e:
            print(e)
            return False

    """
    Retrieves all cameras from the system.

    Returns:
        list: A list of Camera objects representing all cameras in the system.
    """

    def get_all_cameras(self):
        self.__camera_list = self.__DBFacade.get_all_cameras()
        return self.__camera_list

    """
    Starts the streaming process for a specific camera and yields frames.

    Args:
        camera_id (int): The ID of the camera.
        connected_cameras (dict): A dictionary containing the mapping of camera IDs to RTSP URLs.

    Yields:
        dict: A dictionary representing a frame for streaming, containing the following keys:
            - "type" (str): The type of the frame, which is set to "streaming".
            - "cameraID" (int): The ID of the camera.
            - "frame" (bytes): The frame data in bytes format.

    """

    async def start_streaming(self, camera_id, connected_cameras):
        from .camera import Camera
        myCamera = Camera()
        rtsp_url = connected_cameras.get(camera_id)
        async for frame in myCamera.generate_frame(rtsp_url):
            if frame is not None:
                yield {
                    "type": "streaming",
                    "cameraID": camera_id,
                    "frame": frame,
                }
