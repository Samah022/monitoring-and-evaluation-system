# Local DB
import sqlite3
from ...db_connect import session
from ..cameraManagement.cameraEntity import Camera
from ..cameraManagement.criteriaEntity import Criteria


class CameraDB:

    """
    Adds a camera to the database.

    Args:
        name (str): The name of the camera to be added as string.
        link (str): The link of the camera to be added as string.
        criteria (list of str): The list of evaluation criteria associated with the camera. Each criterion should be a string.

    Returns:
        bool: True if the camera is successfully added, False otherwise.

    Raises:
        Exception: If there is an error adding the camera to the database.
    """

    def add_camera(self, name: str, link: str, criteria: list) -> bool:
        try:
            my_camera = Camera(Name=name, Link=link)
            session.add(my_camera)
            session.commit()

            if criteria:
                camera_id = session.query(Camera).order_by(
                    Camera.Camera_ID.desc()).first().Camera_ID
                for item in criteria:
                    criteria = Criteria(Name=item, Camera_ID=camera_id)
                    session.add(criteria)
                session.commit()

            session.close()

            return True

        except Exception as e:
            print("Error adding camera to database:", e)
            return False

    """
    Retrieves information about all cameras from the database.

    Returns:
        list of dictionaries or None: The retrieved camera information as a list of dictionaries, where each dictionary represents a camera entity with the following keys:
            - "id" (int): The camera ID.
            - "name" (str): The name of the camera.
            - "link" (str): The RTSP link to the camera.
            - "criteria" (List[str]): A list of criteria associated with the camera.
        The list is empty if no cameras are found or False if an error occurs.

    Raises:
        Exception: If there is an error connecting to the database or retrieving the data.

    Example:
        [{'id': 1, 'name': 'Camera 1', 'link': 'rtsp://example.com/camera1', 'criteria': ['Criterion 1', 'Criterion 2']},
        {'id': 2, 'name': 'Camera 2', 'link': 'rtsp://example.com/camera2', 'criteria': ['Criterion 3', 'Criterion 4']}]
    """

    def get_all_cameras(self):
        try:
            conn = sqlite3.connect('monitoring-and-evaluation.db')
            cr = conn.cursor()

            sql_query = """
                SELECT * FROM Camera
            """
            cr.execute(sql_query)
            cameras = cr.fetchall()

            camera_entities = []
            for camera in cameras:
                camera_id = camera[0]
                camera_name = camera[1]
                camera_link = camera[2]

                sql_query = """
                    SELECT Name FROM Criteria WHERE Camera_ID = :camera_id
                """
                cr.execute(sql_query, {"camera_id": camera_id})
                criteria = [item[0] for item in cr.fetchall()]

                camera_entity = {
                    "id": camera_id,
                    "name": camera_name,
                    "link": camera_link,
                    "criteria": criteria
                }
                camera_entities.append(camera_entity)

            conn.commit()
            return camera_entities

        except Exception as e:
            print("Error connecting to database or retrieving data:", e)
            return False
