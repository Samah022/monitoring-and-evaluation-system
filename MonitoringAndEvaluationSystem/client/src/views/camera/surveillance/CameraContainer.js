import React, { useState, useEffect } from "react";
import getUrlsByIds from "./filterCamera";
import CameraComponent from "./Camera";
import styles from "./CameraContainer.module.css";
import MoonLoader from "react-spinners/MoonLoader";
import ServicesRequests from "../../../controllers/requestHandler/servicesRequests";

function CameraContainer() {
  const [imageBlobs, setImageBlobs] = useState({});
  const [cameraIDs, setCameraIDs] = useState({});
  const [cameras, setCameras] = useState(null);
  const [isPending, setIsPending] = useState(true);

  const servicesRequests = new ServicesRequests();

  useEffect(() => {
    async function fetchCameras() {
      try {
        const cameras = await servicesRequests.getAllCameras();
        setCameras(cameras);
      } catch (error) {
        console.error("Error:", error);
      }
    }
    fetchCameras();

    return () => {
      servicesRequests.close();
    };
  }, []);

  useEffect(() => {
    const cameraIds = cameras ? Object.keys(cameras) : [];
    const connectedCameras = getUrlsByIds(cameraIds, cameras || {});
    servicesRequests.start_camera_streaming(connectedCameras, (blob, ID) => {
      setImageBlobs((prevImageBlobs) => ({ ...prevImageBlobs, [ID]: blob }));
      setCameraIDs((prevCameraIDs) => ({ ...prevCameraIDs, [ID]: ID }));
    });
  }, [cameras]);

  useEffect(() => {
    setIsPending(!cameras);
  }, [cameras]);

  return (
    <div className={styles.container}>
      {cameras &&
        Object.keys(cameras).map((key) => (
          <CameraComponent
            cameraID={`camera${key}`}
            key={`camera${key}`}
            link={`/cameras/${key}`}
            src={imageBlobs[key]}
            title={`Camera ${key} - ${cameras[key].name}`}
          />
        ))}
      {!cameras && (
        <div className={styles.loading}>
          <MoonLoader
            color="var(--secondary-color)"
            loading={isPending}
            size={150}
          />
        </div>
      )}
    </div>
  );
}

export default CameraContainer;