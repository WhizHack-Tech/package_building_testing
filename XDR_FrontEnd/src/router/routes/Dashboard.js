// =============================================================================================
//  File Name: Dashboard.js
//  Description: Details of the Dashboard router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const DashboardRoutes = [
    // Dashboard
    {
      path: '/dashboard/dashboard',
      component: lazy(() => import('../../views/dashboard/dash')),
      meta: {
        action: 'read',
        resource: 'ADMIN'
      }
    },
    {
        path: '/dashboard/attackevents',
        component: lazy(() => import('../../views/dashboard/analytics')),
        meta: {
          action: 'read',
          resource: 'ADMIN'
        }
      },
      // {
      //   path: '/dashboard/attacks',
      //   component: lazy(() => import('../../views/dashboard/ecommerce')),
      //   meta: {
      //     action: 'read',
      //     resource: 'ADMIN'
      //   },
      //   exact: true
      // },
      {
        path: '/dashboard/networkmap',
        component: lazy(() => import('../../views/dashboard/networkmap')),
        exact: true
      },
      {
        path: '/dashboard/relevantintelligence',
        component: lazy(() => import('../../views/dashboard/relevantintelligence')),
        meta: {
          action: 'read',
          resource: 'ADMIN'
        },
        exact: true
      },
  {
        path: '/dashboard/ml&dldetection',
        component: lazy(() => import('../../views/dashboard/ml_dl_page')),
        meta: {
          action: 'read',
          resource: 'ADMIN'
        },
        exact: true
      }
]

export default DashboardRoutes