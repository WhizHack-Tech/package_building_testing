// =============================================================================================
//  File Name: wazuh.js
//  Description: Details of the wazuh navebar component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Pocket, CheckSquare } from 'react-feather'
export default [
    {
        header: 'Wazuh',
        action: 'read',
        resource: 'wazuh'
    },
    {
        id: 'wazuh_1',
        title: 'wazuh page 1',
        icon: <CheckSquare />,
        action: 'read',
        resource: 'wazuh',
        navLink: '/wazuh/index'
    }
]