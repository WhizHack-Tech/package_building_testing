// =============================================================================================
//  File Name: trace.js
//  Description: Details of the trace navebar component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Aperture, AlertCircle, AlertTriangle, Globe } from 'react-feather'
import traceSrc from "@assets/images/logo/trace.gif"

export default [
    {
        header: 'Trace',
        action: 'read',
        resource: 'trace'
        // imageIcon: traceSrc
    },
    {
        id: 'trace_alert_1',
        title: 'Alerts',
        icon: <Aperture />,
        action: 'read',
        resource: 'trace',
        navLink: '/trace/alerts'
    },
    {
        id: 'trace_event_222',
        title: 'Events',
        icon: <AlertCircle />,
        action: 'read',
        resource: 'trace',
        navLink: '/trace/events'
    },
    {
        id: 'trace_incidents_1',
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