// =============================================================================================
//  File Name: TPThreadFeed.js
//  Description: Details of the TPThreadFeed router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Soar = [
    {
        path: '/tp-thread-feed',
        component: lazy(() => import('../../views/TPThreadFeed'))
    }
]

export default Soar