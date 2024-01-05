// =============================================================================================
//  File Name: dashboard.js
//  Description: Details of the dashboard navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Home, Circle, MessageSquare, BarChart2, Shield, Command, Aperture } from 'react-feather'
export default [
  {
    header: 'Home',
    action: 'read',
    resource: 'ADMIN'
  },
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
    id: 'ml&dldetection',
    title: 'ML & DL Detection',
    icon: <Aperture />,
    action: 'read',
    resource: "ADMIN",
    navLink: '/dashboard/ml&dldetection'
  }

]
