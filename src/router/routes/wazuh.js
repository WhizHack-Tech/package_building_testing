// =============================================================================================
//  File Name: wazuh.js
//  Description: Details of the wazuh router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Wazuh = [
    {
        path: '/wazuh/index',
        component: lazy(() => import('../../views/wazuh')),
        meta: {
            action: 'read',
            resource: 'wazuh'
        }
    }
]

export default Wazuh
