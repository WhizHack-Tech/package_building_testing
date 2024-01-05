// =============================================================================================
//  File Name: nids.js
//  Description: Details of the nids router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Nids = [
  {
    path: '/nids/index',
    component: lazy(() => import('../../views/nids/index')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids/dashboard',
    component: lazy(() => import('../../views/nids/dashboards')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/critical-threats-details',
    component: lazy(() => import('../../views/nids/dashboards/CriticalThreats/criticalThreatsDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/internal-attacks-details',
    component: lazy(() => import('../../views/nids/dashboards/InternalAttacks/InternalAttacksDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/outgoing-botnet-details',
    component: lazy(() => import('../../views/nids/dashboards/OutgoingBotnet/OutgoingBotnetDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/external-attacks-details',
    component: lazy(() => import('../../views/nids/dashboards/ExternalAttacks/ExternalAttacksDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/detected-threat-details',
    component: lazy(() => import('../../views/nids/dashboards/DetectedThreatType/detectedthreatdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/overall-attack-details',
    component: lazy(() => import('../../views/nids/dashboards/OverallAttack/OverallAttackDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/map-details',
    component: lazy(() => import('../../views/nids/dashboards/googleMap/mapDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/top-attacked-details',
    component: lazy(() => import('../../views/nids/dashboards/TopsourceAttackCountries/TopAttackCountriesDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/top-attack-asn-details',
    component: lazy(() => import('../../views/nids/dashboards/TopAttackerASNs/TopAttackerASNsDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/attacker-ips-details',
    component: lazy(() => import('../../views/nids/dashboards/AttackerIPs/attackerIpsDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/most-attacked-ports',
    component: lazy(() => import('../../views/nids/dashboards/MostAttackedPorts/MostAttackedPorts')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/top-services-details',
    component: lazy(() => import('../../views/nids/dashboards/TopAttacks/TopattackservicesDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/top-attacked-city-details',
    component: lazy(() => import('../../views/nids/dashboards/TopAttackerCities/TopAttackercountryDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/top-attacked-countries-details',
    component: lazy(() => import('../../views/nids/dashboards/TopsourceAttackCountries/TopAttackCountriesDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids/alerts',
    component: lazy(() => import('../../views/nids/nids_alerts')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-critical-threats-details',
    component: lazy(() => import('../../views/nids/nids_alerts/CriticalThreats/TotalAttackCountDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-external-attack-count',
    component: lazy(() => import('../../views/nids/nids_alerts/externalattack/ExternalAttacketails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-internal-compromised-details',
    component: lazy(() => import('../../views/nids/nids_alerts/InternalCompromise/InternalCompromiseDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-lateral-movement-details',
    component: lazy(() => import('../../views/nids/nids_alerts/LateralMovement/LateralMovementDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-attack-frequency-details',
    component: lazy(() => import('../../views/nids/nids_alerts/AttackCountlines/AttackcountDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-attacked-Services-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ServiceNames/AttackerServicesDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-attacker-ips-details',
    component: lazy(() => import('../../views/nids/nids_alerts/AtaackerTaregtipslines/IPSdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-attacker-port-details',
    component: lazy(() => import('../../views/nids/nids_alerts/TopAttackerPorts/TopAttackerPortDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-attacker-service-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ThreatClass/AttackerServicesdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-malware-details',
    component: lazy(() => import('../../views/nids/nids_alerts/MalwareType/MalwareTypeDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-mitra-tactick-details',
    component: lazy(() => import('../../views/nids/nids_alerts/MitraTactickName/MitraTactickDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-technique-details',
    component: lazy(() => import('../../views/nids/nids_alerts/MitraTechniqueName/MitraTechniqueDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-geo-location-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/googleMap/mapDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  // ** IDS **//

  {
    path: '/nids-alert-ids-geo-location-details',
    component: lazy(() => import('../../views/nids/nids_alerts/IDS_Tab/googleMap/mapDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alerts-ids-detected-threat-details',
    component: lazy(() => import('../../views/nids/nids_alerts/IDS_Tab/DetectedThreatType/detectedthreatdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alerts-ids-countries-details',
    component: lazy(() => import('../../views/nids/nids_alerts/IDS_Tab/TopScroucecountry/Countriesdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ids-city-details',
    component: lazy(() => import('../../views/nids/nids_alerts/IDS_Tab/City/TopAttackercountryDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ids-ans-details',
    component: lazy(() => import('../../views/nids/nids_alerts/IDS_Tab/ASNDetails/ASNattackerdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-target-port-details',
    component: lazy(() => import('../../views/nids/nids_alerts/IDS_Tab/TargetPort/TargetportDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-target-ips-details',
    component: lazy(() => import('../../views/nids/nids_alerts/IDS_Tab/TargetIp/TargetIpsdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-target-mac-details',
    component: lazy(() => import('../../views/nids/nids_alerts/IDS_Tab/TargetMac/TargetMacdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  //** ML&DL**//
  {
    path: '/nids-alert-ml-dl-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/DetectedThreatType/detectedthreatdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ml-dl-countries-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/TopScroucecountry/Countrydetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ml-dl-ans-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/ASNDetails/Asndetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ml-dl-city-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/City/TopAttackercountryDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ml-dl-geo-location-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/googleMap/mapDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ml-dl-target-ip-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/TargetIp/TargetIPdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ml-dl-target-mac-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/TargetMac/TargetMacdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-alert-ml-dl-target-port-details',
    component: lazy(() => import('../../views/nids/nids_alerts/ML_DL_Tab/TargetPort/Targetportdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  // ** event **//
  {
    path: '/nids/events',
    component: lazy(() => import('../../views/nids/nids_event')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-frequency-details',
    component: lazy(() => import('../../views/nids/nids_event/AttackCountlines/AttackcountDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-attacker-ips-details',
    component: lazy(() => import('../../views/nids/nids_event/AtaackerTaregtipslines/IPSdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-attacked-Services-details',
    component: lazy(() => import('../../views/nids/nids_event/ServiceNames/AttackerServicesDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-port-details',
    component: lazy(() => import('../../views/nids/nids_event/TopAttackerPorts/TopAttackerPortDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },

  // ** IDS-Event **//
  {
    path: '/nids-events-ids-detected-threat-details',
    component: lazy(() => import('../../views/nids/nids_event/IDS_Tab/DetectedThreatType/detectedthreatdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },

  {
    path: '/nids-event-ids-geo-location-details',
    component: lazy(() => import('../../views/nids/nids_event/IDS_Tab/googleMap/mapDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-ids-countries-details',
    component: lazy(() => import('../../views/nids/nids_event/IDS_Tab/TopScroucecountry/Countriesdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-ids-city-details',
    component: lazy(() => import('../../views/nids/nids_event/IDS_Tab/City/TopAttackercountryDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-ids-ans-details',
    component: lazy(() => import('../../views/nids/nids_event/IDS_Tab/ASNDetails/ASNattackerdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-ids-target-ips-details',
    component: lazy(() => import('../../views/nids/nids_event/IDS_Tab/TargetIp/TargetIpsdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-ids-target-mac-details',
    component: lazy(() => import('../../views/nids/nids_event/IDS_Tab/TargetMac/TargetMacdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-event-ids-target-port-details',
    component: lazy(() => import('../../views/nids/nids_event/IDS_Tab/TargetPort/TargetportDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  // ** ML&DL Events ** //
  {
    path: '/nids-events-threattype-ml-dl-details',
    component: lazy(() => import('../../views/nids/nids_event/ML_DL_Tab/DetectedThreatType/detectedthreatdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-events-ml-dl-map-details',
    component: lazy(() => import('../../views/nids/nids_event/ML_DL_Tab/googleMap/mapDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-events-ml-dl-counrty-details',
    component: lazy(() => import('../../views/nids/nids_event/ML_DL_Tab/TopScroucecountry/Countrydetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-events-ml-dl-city-details',
    component: lazy(() => import('../../views/nids/nids_event/ML_DL_Tab/City/TopAttackercountryDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-events-ml-dl-asn-details',
    component: lazy(() => import('../../views/nids/nids_event/ML_DL_Tab/ASNDetails/Asndetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-events-ml-dl-tragetport-details',
    component: lazy(() => import('../../views/nids/nids_event/ML_DL_Tab/TargetPort/Targetportdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-events-ml-dl-traget-ip-details',
    component: lazy(() => import('../../views/nids/nids_event/ML_DL_Tab/TargetIp/TargetIPdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-events-ml-dl-target-mac-details',
    component: lazy(() => import('../../views/nids/nids_event/ML_DL_Tab/TargetMac/TargetMacdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  // ** incident **//
  {
    path: '/nids/incidents',
    component: lazy(() => import('../../views/nids/nids_incident')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-critical-threats-details',
    component: lazy(() => import('../../views/nids/nids_incident/CriticalThreats/TotalAttackCountDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-external-attack-count',
    component: lazy(() => import('../../views/nids/nids_incident/externalattack/ExternalAttacketails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-attacker-ips-details',
    component: lazy(() => import('../../views/nids/nids_incident/AtaackerTaregtipslines/IPSdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-frequency-details',
    component: lazy(() => import('../../views/nids/nids_incident/AttackCountlines/AttackcountDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-internal-compromised-details',
    component: lazy(() => import('../../views/nids/nids_incident/InternalCompromise/InternalCompromiseDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-lateral-movement-details',
    component: lazy(() => import('../../views/nids/nids_incident/LateralMovement/LateralMovementDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-attacked-Services-details',
    component: lazy(() => import('../../views/nids/nids_incident/ServiceNames/AttackerServicesDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-city-details',
    component: lazy(() => import('../../views/nids/nids_incident/TopAttackerPorts/TopAttackerPortDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-threat-class-details',
    component: lazy(() => import('../../views/nids/nids_incident/ThreatClass/AttackerServicesdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-malware-details',
    component: lazy(() => import('../../views/nids/nids_incident/MalwareType/MalwareTypeDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  //  ** IDS_Incident ** //
  {
    path: '/nids-incident-ids-ans-details',
    component: lazy(() => import('../../views/nids/nids_incident/IDS_Tab/ASNDetails/ASNattackerdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ids-city-details',
    component: lazy(() => import('../../views/nids/nids_incident/IDS_Tab/City/TopAttackercountryDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ids-detected-threat-details',
    component: lazy(() => import('../../views/nids/nids_incident/IDS_Tab/DetectedThreatType/detectedthreatdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ids-geo-location-details',
    component: lazy(() => import('../../views/nids/nids_incident/IDS_Tab/googleMap/mapDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-target-ips-details',
    component: lazy(() => import('../../views/nids/nids_incident/IDS_Tab/TargetIp/TargetIpsdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-target-mac-details',
    component: lazy(() => import('../../views/nids/nids_incident/IDS_Tab/TargetMac/TargetMacdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-target-port-details',
    component: lazy(() => import('../../views/nids/nids_incident/IDS_Tab/TargetPort/TargetportDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ids-countries-details',
    component: lazy(() => import('../../views/nids/nids_incident/IDS_Tab/TopScroucecountry/Countriesdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },

  //** ML&DL **/
  {
    path: '/nids-incident-ml-dl-details',
    component: lazy(() => import('../../views/nids/nids_incident/ML_DL_Tab/DetectedThreatType/detectedthreatdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ml-dl-geo-location-details',
    component: lazy(() => import('../../views/nids/nids_incident/ML_DL_Tab/googleMap/mapDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ml-dl-countries-details',
    component: lazy(() => import('../../views/nids/nids_incident/ML_DL_Tab/TopScroucecountry/Countrydetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ml-dl-ans-details',
    component: lazy(() => import('../../views/nids/nids_incident/ML_DL_Tab/ASNDetails/Asndetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ml-dl-city-details',
    component: lazy(() => import('../../views/nids/nids_incident/ML_DL_Tab/City/TopAttackercountryDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ml-dl-target-ip-details',
    component: lazy(() => import('../../views/nids/nids_incident/ML_DL_Tab/TargetIp/TargetIPdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ml-dl-target-mac-details',
    component: lazy(() => import('../../views/nids/nids_incident/ML_DL_Tab/TargetMac/TargetMacdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-ml-dl-target-port-details',
    component: lazy(() => import('../../views/nids/nids_incident/ML_DL_Tab/TargetPort/Targetportdetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids-incident-port-details',
    component: lazy(() => import('../../views/nids/nids_incident/TopAttackerPorts/TopAttackerPortDetails')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  },
  {
    path: '/nids/network-map',
    component: lazy(() => import('../../views/nids/networkmap')),
    meta: {
      action: 'read',
      resource: 'nids'
    }
  }

]

export default Nids
