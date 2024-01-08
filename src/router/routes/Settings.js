 // ================================================================================================
//  File Name: Settings.js
//  Description: Details Pages of the Settings ( Routes ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { lazy } from 'react'

const SettingsRoutes = [
  // Settings
  {
    path: '/settings/plans',
    component: lazy(() => import('../../views/settings/plans'))
  },
  {
    path: '/settings/billing',
    component: lazy(() => import('../../views/settings/billing')),
    exact: true
  },
  {
    path: '/settings/email',
    component: lazy(() => import('../../views/settings/email')),
    exact: true
  },
  {
    path: '/settings/emailconfig',
    component: lazy(() => import('../../views/settings/emailconfig')),
    exact: true
  },
  {
    path: '/settings/billingedit/:id',
    component: lazy(() => import('../../views/settings/billingedit')),
    exact: true
  },
  {
    path: '/settings/planedit/:id',
    component: lazy(() => import('../../views/settings/planedit')),
    exact: true
  },
  // {
  //   path: '/settings/editaccount',
  //   component: lazy(() => import('../../views/settings/editaccount')),
  //   exact: true
  // },
  {
    path: '/settings/application',
    component: lazy(() => import('../../views/settings/application')),
    exact: true
  },
  {
    path: '/settings/editapplication/:id',
    component: lazy(() => import('../../views/settings/editapplication')),
    exact: true
  },
  {
    path: '/settings/plan2',
    component: lazy(() => import('../../views/settings/plan2')),
    exact: true
  },
  {
    path: '/settings/planadd',
    component: lazy(() => import('../../views/settings/plan2/Planadd')),
    exact: true
  }
]

export default SettingsRoutes