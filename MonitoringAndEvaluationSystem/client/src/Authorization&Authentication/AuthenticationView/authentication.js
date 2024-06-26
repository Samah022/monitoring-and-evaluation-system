import React from "react";
import { useState } from "react";
import Logo from "../../views/shared/Logo/logo";
import { useNavigate } from "react-router-dom";
import styles from "./authentication.module.css";
import MainButton from "../../views/shared/MainButton/MainButton";
import { validateLogin } from "../authZicationController/validateLogin";
import ServicesRequests from "../authZicationController/ServicesRequests";
import InputFieldWithLabel from "../../views/shared/InputFieldWithLabel/InputFieldWithLabel";

export default function Auth() {
  const [values, setValues] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [loginError, setLoginError] = useState("");
  const redirectToHome = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();

    const validationErrors = await validateLogin(values);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    const servicesRequests = new ServicesRequests();
    servicesRequests
      .login(values.email, values.password)
      .then((data) => {
        if (data.state) {
          redirectToHome("/");
        } else {
          setLoginError("Incorrect email or password, please try again.");
        }
      })
      .catch((error) => {
        console.error("login error", error);
      });
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setValues((prevValues) => ({ ...prevValues, [name]: value }));
    setErrors((prevErrors) => ({ ...prevErrors, [name]: "" }));
    setLoginError("");
  };

  return (
    <div className={styles.mainContainer}>
      <div className={styles.leftContainer}>
        <p>
          <div className={styles.boldText}>
            Success <br />
            start here
          </div>
          Gain valuable insights and maintain <br />
          high standards by logging into our
          <br />
          advanced quality-monitoring
          <br />
          platform!💡
        </p>
      </div>

      <div className={styles.rightContainer}>
        <Logo />
        <h4>Log in </h4>
        <form className={styles.innerContainer} onSubmit={handleLogin}>
          <InputFieldWithLabel
            color="var(--background-color)"
            type="email"
            width="calc(100vw / 4)"
            inputLabel="Email Address *"
            placeholder="example@gmail.com"
            name="email"
            value={values.email}
            handleChange={handleInputChange}
          />
          {errors.email && (
            <div className={`error ${styles.error}`}>{errors.email}</div>
          )}
          <InputFieldWithLabel
            color="var(--background-color)"
            type="password"
            width="calc(100vw / 4)"
            inputLabel="Password *"
            placeholder="*******"
            name="password"
            value={values.password}
            handleChange={handleInputChange}
          />
          {errors.password && (
            <div className={`error ${styles.error}`}>{errors.password}</div>
          )}
          {loginError && (
            <div className={`error ${styles.error}`}>{loginError}</div>
          )}
          <MainButton
            text="Log in"
            width="calc(100vw / 4)"
            height="calc(100vh / 15)"
            marginTop="30px"
          />
        </form>
      </div>
    </div>
  );
}
