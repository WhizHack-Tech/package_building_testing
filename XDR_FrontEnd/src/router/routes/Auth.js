// =============================================================================================
//  File Name: Auth.js
//  Description: Details of the Auth router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
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
    },
    {
        path: '/generate-new-password/:id',
        component: lazy(() => import('../../views/generateNewPassword')),
        layout: 'BlankLayout',
        meta: {
          authRoute: true
        }
    },
    {
        path: '/mfa-login/:v_token',
        component: lazy(() => import('../../views/mfa_login')),
        layout: 'BlankLayout',
        meta: {
          authRoute: true
        }
    },
    {
        path: '/forgot-password',
        component: lazy(() => import('../../views/forgot_password')),
        layout: 'BlankLayout',
        meta: {
          authRoute: true
        }
    }
]

export default AuthRoutes