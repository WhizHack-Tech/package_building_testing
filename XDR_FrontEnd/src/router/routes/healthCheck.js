// =============================================================================================
//  File Name: healthCheck.js
//  Description: Details of the health Check router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const HealthCheck = [
    {
        path: '/health-check/sensor-health',
        component: lazy(() => import('../../views/healthCheck'))
    },
    {
        path: '/health-check/sensor-types',
        component: lazy(() => import('../../views/healthCheck/charts'))
    },
    {
        path: '/health-check/sensor-details',
        component: lazy(() => import('../../views/healthCheck/charts/LineChart/sensorDetails'))
    }
]

export default HealthCheck