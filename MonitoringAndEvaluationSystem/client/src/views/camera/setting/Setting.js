import Styles from "./Setting.module.css";
import Button from "../../shared/MainButton/MainButton";
import InputFieldWithLabel from "../../shared/InputFieldWithLabel/InputFieldWithLabel";
import SwitchButtonWithLabel from "../../shared/SwitchButtonWithLabel/SwitchButtonWithLabel";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { validateCameraObject } from "./formValidation";
import ServicesRequests from "../../../controllers/requestHandler/servicesRequests";

const Setting = () => {
  const [values, setValues] = useState({
    name: "",
    link: "",
    criteria: [],
  });

  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [isPending, setIsPending] = useState(false);
  const redirectToHome = useNavigate();

  const handleInputChange = (event) => {
    setValues((prev) => {
      let updatedValues = { ...prev };
      if (event.target.name === "criteria") {
        if (event.target.checked) {
          updatedValues.criteria = [...prev.criteria, event.target.value];
        } else {
          updatedValues.criteria = prev.criteria.filter(
            (item) => item !== event.target.value
          );
        }
      } else {
        updatedValues = { ...prev, [event.target.name]: event.target.value };
      }
      return updatedValues;
    });
    setServerError("");
  };

  const handleCameraSubmit = async (e) => {
    e.preventDefault();
    const errors = await validateCameraObject(values);
    setErrors(errors);

    if (Object.keys(errors).length === 0) {
      setIsPending(true);
      const servicesRequests = new ServicesRequests();
      servicesRequests
        .addCamera(values)
        .then((data) => {
          setIsPending(false);
          if (data.state) {
            redirectToHome("/");
          } else {
            setServerError("Error adding camera. Please try again.");
          }
        })
        .catch((error) => {
          setIsPending(false);
          console.error("error", error);
        });
    }
  };

  return (
    <form className={Styles.mainContainer} onSubmit={handleCameraSubmit}>
      <h1 className={Styles.title}>Camera Settings</h1>

      <InputFieldWithLabel
        inputLabel="Camera Name *"
        type="text"
        placeholder="e.g. camera1, cashier camera . . . "
        name="name"
        handleChange={handleInputChange}
      />
      {errors.name && (
        <div className={`error ${Styles.error}`}>{errors.name}</div>
      )}
      <InputFieldWithLabel
        inputLabel="Camera Link *"
        type="text"
        placeholder="e.g. rtsp://ip:port/xxx.xxx"
        name="link"
        handleChange={handleInputChange}
      />
      {errors.link && (
        <div className={`error ${Styles.error}`}>{errors.link}</div>
      )}

      <div className={Styles.innerContainer}>
        <label className={Styles.label}>Evaluation Criteria</label>
        <SwitchButtonWithLabel
          text="1.   Customer Emotions"
          name="criteria"
          value="emotion"
          handleToggle={handleInputChange}
        />
        <SwitchButtonWithLabel
          text="2.   Kitchen Uniforms"
          name="criteria"
          value="uniform"
          handleToggle={handleInputChange}
        />
      </div>
      {serverError && (
        <div className={`error ${Styles.error}`}>{serverError}</div>
      )}
      <div className={Styles.button}>
        {!isPending && (
          <Button
            text="Add Camera"
            width="calc(100vw / 10)"
            height="calc(100vh/15)"
          />
        )}
        {isPending && (
          <Button
            text="Adding Camera..."
            width="calc(100vw / 10)"
            height="calc(100vh/15)"
            disabled
          />
        )}
      </div>
    </form>
  );
};

export default Setting;
