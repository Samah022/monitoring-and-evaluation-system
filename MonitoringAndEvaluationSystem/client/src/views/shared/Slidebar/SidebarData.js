import React from 'react'
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined';

export const SidebarData = [
    {
        title: "Surveillance",
        icon: <HomeOutlinedIcon />,
        link: "/"
    },
    {
        title: "Dashboard",
        icon: <DashboardOutlinedIcon />,
        link: "/dashboard"
    },
    {
        title: "Settings",
        icon: <SettingsOutlinedIcon />,
        link: "/setting"
    },
    {
        title: "Log Out",
        icon: <LogoutOutlinedIcon />,
        link: "/login"
    },

]
