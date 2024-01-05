// =============================================================================================
//  File Name: hids.js
//  Description: Details of the hids navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Aperture, AlertCircle, AlertTriangle } from 'react-feather'
import hidsSrc from "@assets/images/logo/hids.gif"
export default [
    {
        header: 'HIDS',
        action: 'read',
        resource: 'hids'
        // imageIcon: hidsSrc
        // icon: <CheckSquare size={20} className='mr-1'/>
    },
    // {
    //     id: 'hids_1',
    //     title: 'Dashboard',
    //     icon: <CheckSquare />,
    //     action: 'read',
    //     resource: 'hids',
    //     navLink: '/hids/index'
    // },
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
