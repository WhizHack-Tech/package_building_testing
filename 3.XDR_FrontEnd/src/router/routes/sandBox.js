// =============================================================================================
//  File Name: sandBox.js
//  Description: Details of the sandBox router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Soar = [
    {
        path: '/sand-box',
        component: lazy(() => import('../../views/sandBox'))
    }
]

export default Soar