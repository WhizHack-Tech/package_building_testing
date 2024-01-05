// =============================================================================================
//  File Name: soar.js
//  Description: Details of the soar navebar component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Codepen, Codesandbox, Command } from 'react-feather'
export default [
    {
        header: 'Response',
        action: 'read',
        resource: 'soar_route'
    },
    {
        id: 'soar_vertical',
        title: 'SOAR',
        icon: <Codepen />,
        action: 'read',
        resource: 'hids',
        // externalLink: true,
        // newTab: "_blank",
        navLink: '/soar'
        // navLink: 'https://xdr-demo-response.zerohack.in'
    }
]
