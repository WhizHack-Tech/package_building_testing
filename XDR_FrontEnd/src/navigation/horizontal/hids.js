// =============================================================================================
//  File Name: hids.js
//  Description: Details of the hids nav object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Aperture, AlertCircle, AlertTriangle } from 'react-feather'
import hidsSrc from "@assets/images/logo/hids.gif"
export default [
    {
        id: 'hids',
        title: 'HIDS',
        action: 'read',
        resource: 'hids',
        // imageIcon: hidsSrc,
        // icon: <CheckSquare size={20} className='mr-1'/>
        children: [
            {
                id: 'hids_alerts',
                title: 'Alerts',
                icon: <Aperture />,
                action: 'read',
                resource: 'hids',
                navLink: '/hids/alerts'
            },
            {
                id: 'hids_events',
                title: 'Events',
                icon: <AlertCircle />,
                action: 'read',
                resource: 'hids',
                navLink: '/hids/events'
            },
            {
                id: 'hids_incident',
                title: 'Incidents',
                icon: <AlertTriangle />,
                action: 'read',
                resource: 'hids',
                navLink: '/hids/incidents'
            }

        ]
    }
]
