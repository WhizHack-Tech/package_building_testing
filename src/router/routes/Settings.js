// =============================================================================================
//  File Name: Settings.js
//  Description: Details of the Settings router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const SettingsRoutes = [
  // Settings
  {
    path: '/settings/editaccount',
    component: lazy(() => import('../../views/settings/editaccount')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    }
  },
  {
    path: '/settings/reports',
    component: lazy(() => import('../../views/settings/reports')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    }
  },
  {
    path: '/settings/notification',
    component: lazy(() => import('../../views/settings/notification')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    }
  },
  {
    path: '/settings/discover',
    component: lazy(() => import('../../views/settings/discover')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    }
  },
  {
    path: '/settings/reports-exports',
    component: lazy(() => import('../../views/settings/reports_exports/index')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    }
  }
  // {
  //   path: '/settings/wazuh',
  //   component: lazy(() => import('../../views/settings/wazuh')),
  //   meta: {
  //     action: 'read',
  //     resource: 'ADMIN'
  //   }
  // }
  
]

export default SettingsRoutes