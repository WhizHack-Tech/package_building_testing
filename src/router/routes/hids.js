// =============================================================================================
//  File Name: nids.js
//  Description: Details of the nids router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const Hids = [
  {
    path: '/hids/index',
    component: lazy(() => import('../../views/hids/')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids/alerts',
    component: lazy(() => import('../../views/hids/alerts')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-details',
    component: lazy(() => import('../../views/hids/alerts/Views')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids/events',
    component: lazy(() => import('../../views/hids/events')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-event-details',
    component: lazy(() => import('../../views/hids/events/Views')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids/incidents',
    component: lazy(() => import('../../views/hids/incident')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident-details',
    component: lazy(() => import('../../views/hids/incident/Views')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-mitretactic-details',
    component: lazy(() => import('../../views/hids/alerts/MitreTactic/Mitretactic')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-technique-details',
    component: lazy(() => import('../../views/hids/alerts/MitraTechniqueName/MitraTechniqueDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-pic-dss-details',
    component: lazy(() => import('../../views/hids/alerts/MitraPIc/MitrapicDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-event-mitratactick-details',
    component: lazy(() => import('../../views/hids/events/MitraTactickName/MalwareTacticDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-event-technique-details',
    component: lazy(() => import('../../views/hids/events/MitraTechniqueName/MitraTechniqueDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-event-pic-dss-details',
    component: lazy(() => import('../../views/hids/events/Mitrapicdss/MitrapicdssDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-event-anomaly-details',
    component: lazy(() => import('../../views/hids/events/AnomolyDetection/AnomolyDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-event-ransomware-details',
    component: lazy(() => import('../../views/hids/events/RansomwareDetection/RansomwareDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident-technique-details',
    component: lazy(() => import('../../views/hids/incident/MitraTechniqueName/MitraTechniqueDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident-mitratactick-details',
    component: lazy(() => import('../../views/hids/incident/MitraTactickName/MitraTactickDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident-pic-dss-details',
    component: lazy(() => import('../../views/hids/incident/MitePicdss/Mitrepicdssdetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-anomaly-details',
    component: lazy(() => import('../../views/hids/alerts/AnomolyDetection/AnomolyDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-ransomware-details',
    component: lazy(() => import('../../views/hids/alerts/RansomwareDetection/RansomwareDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident-anomaly-details',
    component: lazy(() => import('../../views/hids/incident/AnomolyDetection/AnomolyDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident-ransomware-details',
    component: lazy(() => import('../../views/hids/incident/RansomwareDetection/RansomwareDetails')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  // Alerts Tables //
  {
    path: '/hids-alert-security_events_top_5_alerts',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/Top5alertstable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-security_events_alert_groups_evolution',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/Alertgroupsevolutiontable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-security_events_top_5_groups',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/Top5rulesgroupstable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-security_events_rule_pci_dss',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/Top5PCIDSSTable ')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert-security_events_mitre_attack_tactics',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/AlertGroupTactictable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-alert_mitre_alerts_evolution',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/Mitrealertsevolution')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_alert_rule_mitre_id',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/Rulemitreidtable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_alert_rule_mitre_technique',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/MitreTechniquetable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_alert_rule_mitre_e',
    component: lazy(() => import('../../views/hids/alerts/Views/Tables/MitreTechniquetable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  // Events //
  {
    path: '/hids-event-security_events_top_5_alerts',
    component: lazy(() => import('../../views/hids/events/Views/Tables/Top5alertstable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-events-security_events_top_5_groups',
    component: lazy(() => import('../../views/hids/events/Views/Tables/Top5rulesgroupstable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-events-security_events_rule_pci_dss',
    component: lazy(() => import('../../views/hids/events/Views/Tables/Top5PCIDSSTable ')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-events_security_events_alert_groups_evolution',
    component: lazy(() => import('../../views/hids/events/Views/Tables/Alertgroupsevolutiontable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_event_mitre_alerts_evolution',
    component: lazy(() => import('../../views/hids/events/Views/Tables/Mitrealertsevolution')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_events_rule_mitre_id',
    component: lazy(() => import('../../views/hids/events/Views/Tables/Rulemitreidtable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_event_rule_mitre_technique',
    component: lazy(() => import('../../views/hids/events/Views/Tables/MitreTechniquetable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-event-security_events_mitre_attack_tactics',
    component: lazy(() => import('../../views/hids/events/Views/Tables/MitreAtt&ckTacticstable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  // Incident //
  {
    path: '/hids-incident-security_events_top_5_alerts',
    component: lazy(() => import('../../views/hids/incident/Views/Tables/Top5alertstable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident-security_events_top_5_groups',
    component: lazy(() => import('../../views/hids/incident/Views/Tables/Top5rulesgroupstable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_incidents_security_events_rule_pci_dss',
    component: lazy(() => import('../../views/hids/incident/Views/Tables/Top5PCIDSSTable ')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident_security_events_alert_groups_evolution',
    component: lazy(() => import('../../views/hids/incident/Views/Tables/Alertgroupsevolutiontable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_incident_mitre_alerts_evolution',
    component: lazy(() => import('../../views/hids/incident/Views/Tables/Mitrealertsevolution')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_incident_rule_mitre_id',
    component: lazy(() => import('../../views/hids/incident/Views/Tables/Rulemitreidtable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids_incident_rule_mitre_technique',
    component: lazy(() => import('../../views/hids/incident/Views/Tables/MitreTechniquetable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  },
  {
    path: '/hids-incident-security_events_mitre_attack_tactics',
    component: lazy(() => import('../../views/hids/incident/Views/Tables/MitreAtt&ckTacticstable')),
    exact: true,
    meta: {
      action: 'read',
      resource: 'hids'
    }
  }
]

export default Hids