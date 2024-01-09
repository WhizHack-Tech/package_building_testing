 // ================================================================================================
//  File Name: Faq.js
//  Description: Details Pages of the Faq ( Routes ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { lazy } from 'react'
import { Redirect } from 'react-router-dom'

const FaqRoutes = [
  // Dashboards
  {
    path: '/faq/add',
    component: lazy(() => import('../../views/faq/add'))
  },
  {
    path: '/faq/faq',
    component: lazy(() => import('../../views/faq/faq')),
    exact: true
  },
  {
    path: '/faq/user/list',
    component: lazy(() => import('../../views/faq/user/list'))
  },
  {
    path: '/faq/user/edit',
    exact: true,
    component: () => <Redirect to='/faq/user/edit/1' />
  },
  {
    path: '/faq/user/edit/:id',
    component: lazy(() => import('../../views/faq/user/edit')),
    meta: {
      navLink: '/faq/user/edit'
    }
  },
  {
    path: '/faq/user/view',
    exact: true,
    component: () => <Redirect to='/faq/user/view/1' />
  },
  {
    path: '/faq/user/view/:id',
    component: lazy(() => import('../../views/faq/user/view')),
    meta: {
      navLink: '/faq/user/view'
    }
  }
]

export default FaqRoutes
