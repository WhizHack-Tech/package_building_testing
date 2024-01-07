// =============================================================================================
//  File Name: tpSource.js
//  Description: Details of the tpSource router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Soar = [
    {
        path: '/tp-source',
        component: lazy(() => import('../../views/tpSource'))
    }
]

export default Soar