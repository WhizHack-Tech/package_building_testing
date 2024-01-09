// ================================================================================================
//  File Name: dashboard.js
//  Description: Details Pages of the Navigtion ( Horizontal ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Home, BarChart2, Shield } from 'react-feather'

export default [
  {
    id: 'home',
    title: 'Home',
    icon: <Home />,
    children: [
          // {
          //   id: 'h-dashboard',
          //   title: 'Dashboard',
          //   icon: <BarChart2 />,
          //   navLink: '/dashboard/dashboard',
          //   action: 'read',
          //   resource: 'ADMIN'
          // },
          {
            id: 'agnetDash',
            title: 'Agents',
            icon: <Shield />,
            navLink: '/dashboard/agent',
            action: 'read',
            resource: 'ADMIN'
          }
    ]
  }
     
]