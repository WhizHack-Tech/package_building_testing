// =============================================================================================
//  File Name: nids.js
//  Description: Details of the nids navebar component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Aperture, AlertCircle, AlertTriangle, Activity } from 'react-feather'
import nidsSrc from "@assets/images/logo/nids.gif"
import nidsalert from "@assets/images/logo/latest.svg"
// import nidsalert from "@assets/images/logo/alertcopy.svg" 
export default [
    {
        header: 'NIDS',
        action: 'read',
        resource: 'nids'
        // imageIcon: nidsSrc
    },
    // {
    //     id: 'nids_1',
    //     title: 'Dashboard',
    //     icon: <CheckSquare />,
    //     action: 'read',
    //     resource: 'nids',
    //     navLink: '/nids/dashboard'
    // },
    {
        id: 'nids_2',
        title: 'Alerts',
        icon: <Aperture />,
        // imageIcon: nidsalert,
        action: 'read',
        resource: 'nids',
        navLink: '/nids/alerts'
    },
    {
        id: 'nids_3',
        title: 'Events',
        icon: <AlertCircle />,
        action: 'read',
        resource: 'nids',
        navLink: '/nids/events'
    },
    {
        id: 'nids_4',
        title: 'Incidents',
        icon: <AlertTriangle />,
        action: 'read',
        resource: 'nids',
        navLink: '/nids/incidents'
    },
    {
        id: 'nids_5',
        title: 'Network Map',
        icon: <Activity />,
        action: 'read',
        resource: 'nids',
        navLink: '/nids/network-map'
    }
]