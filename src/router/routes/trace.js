// =============================================================================================
//  File Name: trace.js
//  Description: Details of the trace router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Trace = [
    {
        path: '/trace/alerts',
        component: lazy(() => import('../../views/trace/trace_alerts')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace/events',
        component: lazy(() => import('../../views/trace/trace_events')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace/incidents',
        component: lazy(() => import('../../views/trace/trace_incidents')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace/globalthreatfeed',
        component: lazy(() => import('../../views/trace/global_threat_feed')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    // ** Alert ** //
    {
        path: '/trace-alert-critical-threats-details',
        component: lazy(() => import('../../views/trace/trace_alerts/CriticalThreats/TotalAttackCountDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-lateral-movement-details',
        component: lazy(() => import('../../views/trace/trace_alerts/LateralMovement/LateralMovementDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-geo-location-details',
        component: lazy(() => import('../../views/trace/trace_alerts/googleMap/mapDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-external-attack-details',
        component: lazy(() => import('../../views/trace/trace_alerts/externalattack/ExternalAttacketails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-internal-compromised-details',
        component: lazy(() => import('../../views/trace/trace_alerts/InternalCompromise/InternalCompromiseDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-attacker-port-details',
        component: lazy(() => import('../../views/trace/trace_alerts/AttackerPorts/TopAttackerPortDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-attacker-ips-details',
        component: lazy(() => import('../../views/trace/trace_alerts/AtaackerTaregtipslines/IPSdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-ans-details',
        component: lazy(() => import('../../views/trace/trace_alerts/ASNDetails/ASNattackerdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-city-details',
        component: lazy(() => import('../../views/trace/trace_alerts/City/TopAttackercountryDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alerts-countries-details',
        component: lazy(() => import('../../views/trace/trace_alerts/TopScroucecountry/Countriesdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-target-ips-details',
        component: lazy(() => import('../../views/trace/trace_alerts/TargetIp/TargetIpsdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-alert-target-port-details',
        component: lazy(() => import('../../views/trace/trace_alerts/TargetPort/TargetportDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
     // ** Events ** //
     {
        path: '/trace-events-critical-threats-details',
        component: lazy(() => import('../../views/trace/trace_events/CriticalThreats/TotalAttackCountDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-lateral-movement-details',
        component: lazy(() => import('../../views/trace/trace_events/LateralMovement/LateralMovementDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-geo-location-details',
        component: lazy(() => import('../../views/trace/trace_events/googleMap/mapDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-external-attack-details',
        component: lazy(() => import('../../views/trace/trace_events/externalattack/ExternalAttacketails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-internal-compromised-details',
        component: lazy(() => import('../../views/trace/trace_events/InternalCompromise/InternalCompromiseDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-attacker-port-details',
        component: lazy(() => import('../../views/trace/trace_events/AttackerPorts/TopAttackerPortDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-attacker-ips-details',
        component: lazy(() => import('../../views/trace/trace_events/AtaackerTaregtipslines/IPSdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-ans-details',
        component: lazy(() => import('../../views/trace/trace_events/ASNDetails/ASNattackerdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-city-details',
        component: lazy(() => import('../../views/trace/trace_events/City/TopAttackercountryDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-countries-details',
        component: lazy(() => import('../../views/trace/trace_events/TopScroucecountry/Countriesdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-target-ips-details',
        component: lazy(() => import('../../views/trace/trace_events/TargetIp/TargetIpsdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-events-target-port-details',
        component: lazy(() => import('../../views/trace/trace_events/TargetPort/TargetportDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },

    // ** Incidents ** //
     {
        path: '/trace-incident-critical-threats-details',
        component: lazy(() => import('../../views/trace/trace_incidents/CriticalThreats/TotalAttackCountDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-lateral-movement-details',
        component: lazy(() => import('../../views/trace/trace_incidents/LateralMovement/LateralMovementDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-geo-location-details',
        component: lazy(() => import('../../views/trace/trace_incidents/googleMap/mapDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-external-attack-details',
        component: lazy(() => import('../../views/trace/trace_incidents/externalattack/ExternalAttacketails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-internal-compromised-details',
        component: lazy(() => import('../../views/trace/trace_incidents/InternalCompromise/InternalCompromiseDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-attacker-port-details',
        component: lazy(() => import('../../views/trace/trace_incidents/AttackerPorts/TopAttackerPortDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-attacker-ips-details',
        component: lazy(() => import('../../views/trace/trace_incidents/AtaackerTaregtipslines/IPSdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-ans-details',
        component: lazy(() => import('../../views/trace/trace_incidents/ASNDetails/ASNattackerdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-city-details',
        component: lazy(() => import('../../views/trace/trace_incidents/City/TopAttackercountryDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-countries-details',
        component: lazy(() => import('../../views/trace/trace_incidents/TopScroucecountry/Countriesdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-target-ips-details',
        component: lazy(() => import('../../views/trace/trace_incidents/TargetIp/TargetIpsdetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-incident-target-port-details',
        component: lazy(() => import('../../views/trace/trace_incidents/TargetPort/TargetportDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    // ** Gobal ** //

    {
        path: '/trace-gobal-malware-details',
        component: lazy(() => import('../../views/trace/global_threat_feed/Malware/TopAttackercountryDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-gobal-intel-source-details',
        component: lazy(() => import('../../views/trace/global_threat_feed/Intelsource/IntelSouecedetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    },
    {
        path: '/trace-gobal-threat-type-source-details',
        component: lazy(() => import('../../views/trace/global_threat_feed/Threattype/ThreattypeDetails')),
        meta: {
            action: 'read',
            resource: 'trace'
        }

    }

]

export default Trace
