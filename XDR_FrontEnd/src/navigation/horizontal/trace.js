// =============================================================================================
//  File Name: trace.js
//  Description: Details of the trace navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Aperture, AlertCircle, AlertTriangle, Globe } from 'react-feather'
import traceSrc from "@assets/images/logo/trace.gif"

export default [
    {
        id: 'trace',
        title: 'Trace',
        action: 'read',
        resource: 'trace',
        // imageIcon: traceSrc,
        children: [
            {
                id: 'trace_alert_1',
                title: 'Alerts',
                icon: <Aperture />,
                action: 'read',
                resource: 'trace',
                navLink: '/trace/alerts'
            },
            {
                id: 'trace_2',
                title: 'Events',
                icon: <AlertCircle />,
                action: 'read',
                resource: 'trace',
                navLink: '/trace/events'
            },
            {
                id: 'trace_3',
                title: 'Incidents',
                icon: <AlertTriangle />,
                action: 'read',
                resource: 'trace',
                navLink: '/trace/incidents'
            },
            {
                id: 'trace_4',
                title: 'Global Threat Feed',
                icon: <Globe />,
                action: 'read',
                resource: 'trace',
                navLink: '/trace/globalthreatfeed'
            }
        ]
    }
]