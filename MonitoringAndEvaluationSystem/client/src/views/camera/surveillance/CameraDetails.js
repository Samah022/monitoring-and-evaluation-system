import React from "react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import getUrlsByIds from "./filterCamera";
import styles from "./CameraDetails.module.css";
import MoonLoader from "react-spinners/MoonLoader";
import CloseOutlinedIcon from "@mui/icons-material/CloseOutlined";
import ServicesRequests from "../../../controllers/requestHandler/servicesRequests";

function CameraDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [imageBlob, setImageBlob] = useState(null);
  const [cameraID, setCameraID] = useState(null);

  const [cameras, setCameras] = useState(null);
  const [isPending, setIsPending] = useState(true);

  const [currantCamera, setCurrantCamera] = useState(null);

  const servicesRequests = new ServicesRequests();

  useEffect(() => {
    async function fetchCameras() {
      try {
        const cameras = await servicesRequests.getAllCameras();
        setCameras(cameras);
        setCurrantCamera(cameras[id]);
      } catch (error) {
        console.error("Error:", error);
      }
    }
    fetchCameras();
  }, []);

  useEffect(() => {
    const connectedCameras = getUrlsByIds([`${id}`], cameras || {});
    servicesRequests.start_camera_streaming(
      connectedCameras,
      (blob, receivedID) => {
        if (receivedID == id) {
          setImageBlob(URL.createObjectURL((blob)));
          setCameraID(receivedID);
        }
      }
    );
    return () => {
      servicesRequests.close();
    };
  }, [cameras]);

  useEffect(() => {
    setIsPending(!currantCamera);
  }, [currantCamera]);

  function handleCloseCamera() {
    navigate("/");
  }

  return (
    <>
      {isPending && (
        <div className={styles.loading}>
          <MoonLoader color="var(--secondary-color)" loading={isPending} size={150}/>
        </div>
      )}
      {!isPending && (
        <div className={styles.container}>
          <div className={styles.header}>
            <div className={styles.label}>
              Camera {id} - {currantCamera.name}
            </div>
            <CloseOutlinedIcon className={styles.closeIcon}  onClick={handleCloseCamera} />
          </div>
          {imageBlob && (
            <img className={styles.image} src={imageBlob} alt={currantCamera.url}/>
          )}
          {!imageBlob && (
            <div className={styles.loading}>
              <MoonLoader color="var(--secondary-color)" loading={true} size={150}/>
            </div>
          )}
        </div>
      )}
    </>
  );
}

export default CameraDetails;
