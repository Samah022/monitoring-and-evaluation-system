import React from "react";
import Logo from "../Logo/logo";
import styles from "./Sidebar.module.css";
import { NavLink } from "react-router-dom";
import { SidebarData } from "./SidebarData";

import ServicesRequests from "../../../Authorization&Authentication/authZicationController/ServicesRequests";

const handleLogout = async () => {
  event.preventDefault();

  try {
    const servicesRequests = new ServicesRequests();
    await servicesRequests.logout();
    console.log("logging out: done");
  } catch (error) {
    console.error("Error logging out:", error);
  }
};

function Sidebar() {
  return (
    <div className={styles.sidebar}>
      <Logo width="100px" height="100px" />
      <ul className={styles.sidebarList}>
        {SidebarData.map((val, key) => (
          <NavLink
            key={key}
            className={`${styles.sidebarRow} ${
              window.location.pathname === val.link ? styles.active : ""
            }`}
            to={val.link}
            onClick={() => val.title === "Log Out" && handleLogout()}
          >
            <div className={styles.icon}>{val.icon}</div>
            <div className={styles.title}>{val.title}</div>
          </NavLink>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;
