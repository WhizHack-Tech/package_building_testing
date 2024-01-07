// =============================================================================================
//  File Name: liveMaps.js
//  Description: Details of the liveMaps router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const LiveMaps = [
    {
        path: '/live/map',
        component: lazy(() => import('../../views/liveMaps'))
    }
]

export default LiveMaps