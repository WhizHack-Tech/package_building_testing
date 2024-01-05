// =============================================================================================
//  File Name: soar.js
//  Description: Details of the soar router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Soar = [
    {
        path: '/soar',
        component: lazy(() => import('../../views/soar/index'))
    }
]

export default Soar