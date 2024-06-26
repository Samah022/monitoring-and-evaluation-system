import uvicorn
from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
# create the DB
from .startup import create_tables_on_startup
# from .controllers.camera.camera import Camera
from server.controllers.camera.camera import Camera
from .controllers.user.user import User
from .authZication.authZicationController.authenticator import Authenticator
from .controllers.servicesHandler.servicesHandler import ServicesHandler

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

servicesHandler = ServicesHandler()


authenticator = Authenticator()

# @app.on_event("startup")
# async def startup_event():
#     create_tables_on_startup()


@app.post("/add_camera")
async def add_camera(request: Request):
    camera_data = await request.json()
    new_camera = Camera(
        camera_name=camera_data["name"], camera_URL=camera_data["link"], evaluation_criteria=camera_data["criteria"])
    return servicesHandler.handle_add_camera(new_camera)


@app.websocket("/dashboard")
async def fetch_dashboard_data(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        if data["type"] == "getDashboardData":
            async for chart_data in servicesHandler.handle_fetch_dashboard_data():
                await websocket.send_json(chart_data)


@app.get("/get_all_cameras")
def get_all_cameras():
    return servicesHandler.handle_get_all_cameras()


@app.get("/isAuthenticated")
def is_authenticated():
    user = servicesHandler.handle_connected_user()
    if user.get_authenticated():
        return {"state": True}
    return {"state": False}


@app.post("/login")
async def login(request: Request):
    credentials = await request.json()
    user = servicesHandler.handle_connected_user()
    user.set_email(credentials["email"])
    user.set_password(credentials["password"])
    if not authenticator.login(user):
        return {"state": False}
    return {"state": True}


@app.get("/logout")
def logout():
    user = servicesHandler.handle_connected_user()
    if authenticator.logout(user):
        return {"state": True}
    return {"state": False}


@app.websocket("/streaming")
async def start_streaming(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if data["type"] == "video_feed":
            connected_cameras = data["value"]
            await servicesHandler.handle_start_streaming(connected_cameras, websocket)


dev = False
if __name__ == "__main__":
    if dev:
        uvicorn.run("main:app", port=8000, host="localhost", reload=True)
    else:
        uvicorn.run(app, port=8000, host="localhost")
