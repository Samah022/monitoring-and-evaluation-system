from .controllers.camera.camera import Camera
from .controllers.servicesHandler.servicesHandler import ServicesHandler
import asyncio
import multiprocessing
import time

servicesHandler = ServicesHandler()
activated_cameras = []


def process_camera(camera):
    asyncio.run(camera.analysis_frame())


def run_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()


def process_cameras():
    global activated_cameras
    cameras = servicesHandler.handle_get_all_cameras()["data"]

    activated_cameras.clear()

    for camera in cameras:
        for index, criteria in enumerate(camera["criteria"]):
            activated_camera = Camera(ID=camera["id"], camera_name=camera["name"],
                                      camera_URL=camera["link"], evaluation_criteria=[camera["criteria"][index]])
            activated_cameras.append(activated_camera)

    processes = []
    for activated_camera in activated_cameras:
        process = multiprocessing.Process(
            target=process_camera, args=(activated_camera,))
        process.start()
        processes.append(process)

    run_event_loop()


def check_camera_list():
    global process_cameras_process
    last_length = len(activated_cameras)
    process_cameras_process = multiprocessing.Process(target=process_cameras)
    process_cameras_process.start()
    while True:
        time.sleep(5)
        current_length = len(servicesHandler.handle_get_all_cameras()["data"])
        if current_length != last_length:
            print("New Camera has been added.")
            if process_cameras_process:
                process_cameras_process.terminate()
            process_cameras_process = multiprocessing.Process(
                target=process_cameras)
            process_cameras_process.start()
            last_length = current_length


if __name__ == "__main__":
    check_camera_list()
