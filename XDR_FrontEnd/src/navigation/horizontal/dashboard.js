// =============================================================================================
//  File Name: dashboard.js
//  Description: Details of the dashboard nav object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Home, BarChart2, Shield, Command, Activity, Aperture } from 'react-feather'
export default [
  {
    id: 'home',
    title: 'Home',
    icon: <Home />,
    children: [
      {
        id: 'Dash',
        title: 'Dashboard',
        icon: <BarChart2 />,
        action: 'read',
        resource: 'ADMIN',
        navLink: '/dashboard/dashboard'
      },
          {
            id: 'analyticsDash',
            title: 'Attack Events',
            icon: <Shield />,
            action: 'read',
            resource: 'ADMIN',
            navLink: '/dashboard/attackevents'
          },
          {
            id: 'relevantintelligence',
            title: 'Intelligence',
            icon: <Command />,
            action: 'read',
            resource: "ADMIN",
            navLink: '/dashboard/relevantintelligence'
          },
          {
            id: 'networkmap',
            title: 'Network Map',
            icon: <Activity />,
            navLink: '/dashboard/networkmap'
          },
          {
            id: 'ml&dldetection',
            title: 'ML & DL Detection',
            icon: <Aperture />,
            action: 'read',
            resource: "ADMIN",
            navLink: '/dashboard/ml&dldetection'
          }
    ]
  }
]
