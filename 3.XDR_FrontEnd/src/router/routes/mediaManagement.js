// =============================================================================================
//  File Name: mediaManagement.js
//  Description: Details of the mediaManagement router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const mediaManagement = [
    {
        path: '/media-management',
        component: lazy(() => import('../../views/mediaManagement'))
    }
]

export default mediaManagement