 // ================================================================================================
//  File Name: Dashboard.js
//  Description: Details Pages of the Dashboard ( Routes ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { lazy } from 'react'

const DashboardRoutes = [
  // Dashboards
  // {
  //   path: '/dashboard/dashboard',
  //   component: lazy(() => import('../../views/dashboard/analytics')),
  //   meta: {
  //     action: 'read',
  //     resource: 'ADMIN'
  //   }  
  // },
  {
    path: '/dashboard/agent',
    exact: true,
    component: lazy(() => import('../../views/dashboard/agent')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    } 
  },
  {
    path: '/dashboard/agentdetails/:org_location',
    exact: true,
    component: lazy(() => import('../../views/dashboard/agentdetails')),
    meta: {
      navLink: '/dashboard/agentdetails',
      action: 'read',
      resource: 'ADMIN'
    }
  }

 
]

export default DashboardRoutes
