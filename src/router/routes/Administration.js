 // ================================================================================================
//  File Name: Administration.js
//  Description: Details Pages of the Administration ( Routes ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { lazy } from 'react'
import { Redirect } from 'react-router-dom'
const AdministrationRoutes = [
  // Dashboards
  {
    path: '/administration/user/list',
    component: lazy(() => import('../../views/administration/user/list')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    } 
  },
  {
    path: '/administration/user/view/:id/:activated_plan_id',
    component: lazy(() => import('../../views/administration/user/view')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    } 
  },
  {
    path: '/administration/user/edit/:id',
    component: lazy(() => import('../../views/administration/user/edit'))
  },
  {
    path: '/administration/userconfig/list',
    component: lazy(() => import('../../views/administration/userconfig/list')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    } 
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
  {
    path: '/administration/userconfig/view/:id',
    component: lazy(() => import('../../views/administration/userconfig/view'))
  },  
  {
    path: '/administration/emailconfig',
    component: lazy(() => import('../../views/administration/emailconfig')),
    exact: true
  },
  {
    path: '/administration/account-settings',
    component: lazy(() => import('../../views/administration/account-settings'))
  },  
  // {
  //   path: '/administration/roles',
  //   component: lazy(() => import('../../views/administration/roles')),
  //   meta: {
  //     action: 'read',
  //     resource: 'ADMIN'
  //   } 
  // },
  {
    path: '/administration/permission',
    exact: true,
    component: () => <Redirect to='/administration/permission/1' />
  },
  {
    path: '/administration/permission/:id',
    component: lazy(() => import('../../views/administration/permission')),
    meta: {
      navLink: '/administration/permission'
    }
  },
  {
    path: '/addlocation',
    component: lazy(() => import('../../views/administration/org_location')),
    meta: {
      navLink: '/addlocation'
    }
  },
  {
    path: '/administration/logs',
    component: lazy(() => import('../../views/administration/logs')),
    meta: {
      action: 'read',
      resource: 'ADMIN'
    } 
  }
]

export default AdministrationRoutes