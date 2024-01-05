// =============================================================================================
//  File Name: liveMaps/index.js
//  Description: Details of the liveMaps navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Globe } from 'react-feather'
export default [
    {
        header: 'Live Maps',
        action: 'read',
        resource: 'live_maps'
    },
    {
        id: 'live_maps',
        title: 'Live Attack Map',
        icon: <Globe />,
        action: 'read',
        resource: 'live_maps',
        navLink: '/live/map'
    }
]
