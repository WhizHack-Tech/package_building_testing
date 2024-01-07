// =============================================================================================
//  File Name: healthCheck.js
//  Description: Details of the health Check navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Codepen, Codesandbox, Command } from 'react-feather'
export default [
    {
        header: 'Health Check',
        action: 'read',
        resource: 'health_check'
    },
    {
        id: 'sensor_health_check',
        title: 'Sensor Health',
        icon: <Codepen />,
        action: 'read',
        resource: 'hids',
        navLink: '/health-check/sensor-health'
    }
]
