import React from 'react';
import { useState, useEffect } from 'react';
import styles from "./Camera.module.css";
import { Link } from "react-router-dom";
import ZoomInMapIcon from '@mui/icons-material/ZoomInMap';
import MoonLoader from "react-spinners/MoonLoader";

function Camera(props) {
  const [imageBlob, setImageBlob] = useState(" ");
  const [isPending, setIsPending] = useState(true);

  useEffect(() => {
    if (props.src instanceof Blob) {
      setImageBlob(URL.createObjectURL(props.src));
      setIsPending(false)
    }
    return () => {
      URL.revokeObjectURL(imageBlob);
    };
  }, [props.src]);

  return (
    <Link className={styles.container} to={props.link}>
      <p className={styles.header}>{props.title}</p>
      {!isPending && (
      <img id={props.cameraID}  className={styles.image} src={imageBlob} />
      )} 
      {isPending && (
        <div className={styles.loading}>          
          <MoonLoader
            color="var(--secondary-color)"
            loading={isPending}
            size={150}
          />
        </div>
      )}
      <ZoomInMapIcon className={styles.zoomInMapIcon} />
    </Link>
  );
}

export default Camera;

