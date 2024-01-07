// =============================================================================================
//  File Name: Administration.js
//  Description: Details of the Administration router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'
import { Redirect } from 'react-router-dom'

const AdministartionRoutes = [
  {
    path: '/administration/userconfig/list',
    component: lazy(() => import('../../views/administration/userconfig/list'))
  },
  {
    path: '/administration/userconfig/edit',
    exact: true,
    component: () => <Redirect to='/administration/userconfig/edit/1' />
  },
  {
    path: '/administration/userconfig/edit/:id',
    component: lazy(() => import('../../views/administration/userconfig/edit')),
    meta: {
      navLink: '/administration/userconfig/edit'
    }
  },
  // {
  //   path: '/administration/userconfig/view',
  //   exact: true,
  //   component: () => <Redirect to='/administration/userconfig/view/1' />
  // },
  // {
  //   path: '/administration/userconfig/view/:id',
  //   component: lazy(() => import('../../views/administration/userconfig/view')),
  //   meta: {
  //     navLink: '/administration/userconfig/view'
  //   }
  // },
  {
    path: '/administration/userconfig/view/:id',
    component: lazy(() => import('../../views/administration/userconfig/view'))
  },
  {
    path: '/administration/logs',
    component: lazy(() => import('../../views/administration/logs'))
  },
  {
    path: '/administration/Api-key',
    component: lazy(() => import('../../views/administration/Api-key'))
  }
  // {
  //   path: '/administration/shop',
  //   className: 'ecommerce-application',
  //   component: lazy(() => import('../../views/administration/shop'))
  // },
  // {
  //   path: '/administration/detail/:id',
  //   component: lazy(() => import('../../views/administration/detail'))
  // }
]

export default AdministartionRoutes
