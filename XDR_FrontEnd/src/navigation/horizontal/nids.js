// =============================================================================================
//  File Name: nids.js
//  Description: Details of the nids navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Pocket, AlertTriangle, AlertOctagon, AlertCircle, Activity } from 'react-feather'
import nidsSrc from "@assets/images/logo/nids.gif"
export default [
    {
        id: 'nids',
        title: 'NIDS',
        action: 'read',
        resource: 'nids',
        // imageIcon: nidsSrc,
        children: [
            {
                id: 'nids_2',
                title: 'Alerts',
                icon: <AlertOctagon />,
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
    }
]