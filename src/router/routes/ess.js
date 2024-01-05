// =============================================================================================
//  File Name: ess.js
//  Description: Details of the ess router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Soar = [
    {
        path: '/ess',
        component: lazy(() => import('../../views/ess'))
    }
]

export default Soar