 // ================================================================================================
//  File Name: Auth.js
//  Description: Details Pages of the Auth ( Routes ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { lazy } from 'react'

const AuthRoutes = [
    {
        path: '/login',
        component: lazy(() => import('../../views/Login')),
        layout: 'BlankLayout',
        meta: {
          authRoute: true
        }
    }
]

export default AuthRoutes