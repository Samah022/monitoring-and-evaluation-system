import React from "react";
import styles from "./App.module.css";
import Sidebar from "./views/shared/Slidebar/Sidebar";
import Dashboard from "./views/dashboard/Dashboard";
import Setting from "./views/camera/setting/Setting";
import CameraDetails from "./views/camera/surveillance/CameraDetails";
import CameraContainer from "./views/camera/surveillance/CameraContainer";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./controllers/viewsController/ProtectedRoute";
import Auth from "./Authorization&Authentication/AuthenticationView/authentication";

function App() {
  return (
    <BrowserRouter>
      <div className={styles.App}>
        <Routes>
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={ <> <Sidebar /> <CameraContainer /> </>} exact />
            <Route path="/cameras/:id" element={<CameraDetails />} />
            <Route path="/dashboard" element={<> <Sidebar /> <Dashboard /> </>} />
            <Route path="/setting" element={<> <Sidebar /> <Setting /> </>} />
          </Route>
          <Route path="/login" element={<Auth />} />
          <Route path='*' element={<Navigate to='/login'/>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;