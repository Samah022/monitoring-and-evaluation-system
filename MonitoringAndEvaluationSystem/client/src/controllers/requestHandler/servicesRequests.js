
export default class ServicesRequests {
  socket = null

  addCamera(values) {
    return new Promise((resolve, reject) => {
      fetch('http://localhost:8000/add_camera', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json(); 
        })
        .then(data => {
          resolve(data); 
        })
        .catch(error => {
          console.error('Error adding camera:', error.message);
          reject(error); 
        });
    });
  }

  fetch_dashboard_data(chartType) {
    this.socket = new WebSocket("ws://localhost:8000/dashboard");
    if (this.socket) {
    return new Promise((resolve, reject) => {
        this.socket.addEventListener("open", () => {
            this.socket.send(JSON.stringify({ type: "getDashboardData" }));
        });

        this.socket.addEventListener("message", (event) => {
            try {
                const data = JSON.parse(event.data);
                const receivedChartType = data.type;

                if (receivedChartType === chartType) {
                    let result = data.data;
                    let objectResult = {
                        "name": receivedChartType,
                        "data": result,
                    };
                    resolve(objectResult);
                }
            } catch (error) {
                console.error("Error parsing message:", error);
                reject(error);
            }
        });
    });
  }}

  async getAllCameras() {

    try {
      const response = await fetch('http://127.0.0.1:8000/get_all_cameras', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      console.log(data.data)

      const cameras = {};
      data.data.forEach(camera => {
        cameras[camera.id] = {
          name: camera.name,
          url: camera.link
        };
      });
      return cameras;

    } catch (error) {
      console.error('Error in getting cameras:', error.message);
      throw error;
    }
  }

  start_camera_streaming(connectedCameras, callback) {
    this.socket = new WebSocket("ws://localhost:8000/streaming");
    if (this.socket) {
      this.socket.addEventListener("open", () => {
        this.socket.send(
          JSON.stringify({
            type: "video_feed",
            value: connectedCameras,
          })
        );
      });

      this.socket.addEventListener("message", (event) => {
        const data = JSON.parse(event.data);
        const cameraID = data.cameraID;
        const frameBase64String = data.frame;
        const type = data.type
        if (type == "streaming" ){
          const bytes = new Uint8Array(
            atob(frameBase64String)
              .split("")
              .map((char) => char.charCodeAt(0))
          );
          const blob = new Blob([bytes], { type: "image/jpeg" });
          callback(blob, cameraID); 
        }
      });
    } else {
      console.error("WebSocket connection could not be initialized.");
    }
  }

  close() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    } else {
      console.error("WebSocket connection is not initialized.");
    }
  }
}
