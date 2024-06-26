import React, { useState, useEffect } from "react";
import { Navigate, Outlet } from "react-router-dom";
import MoonLoader from "react-spinners/MoonLoader";
import ServicesRequests from "../../Authorization&Authentication/authZicationController/ServicesRequests";

const ProtectedRoute = () => {
  const [authState, setAuthState] = useState(null);

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const servicesRequests = new ServicesRequests();
        const isAuthenticated = await servicesRequests.isAuthenticated();
        setAuthState(isAuthenticated.state);
      } catch (error) {
        setAuthState(false);
      }
    };
    checkAuthentication();
  }, []);

  return authState === null ? (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        width: "100vw",
      }}
    >
      <MoonLoader color="var(--secondary-color)" loading={true} size={150} />
    </div>
  ) : authState ? (
    <Outlet />
  ) : (
    <Navigate to="/login" />
  );
};

export default ProtectedRoute;
