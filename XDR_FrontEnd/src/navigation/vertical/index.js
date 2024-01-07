// =============================================================================================
//  File Name: vertical/index.js
//  Description: Details of the navbar index component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Navigation sections imports

// import dashboard from './dashboard'
import administartion from './administartion'
// import settings from './settings'
import report from './report'
import trace from './trace'
// import wazuh from './wazuh'
import nids from './nids'
import hids from './hids'
import liveMaps from './liveMaps'
import healthCheck from './healthCheck'
import soar from './soar'
import mediaManagement from './mediaManagement'
import TPThreadFeed from './TPThreadFeed'
import sandBox from './sandBox'
import ess from './ess'
import tpSource from './tpSource'

// ** Merge & Export

const NavigationLinks = (props) => {
    const navigationLinksList = []

    if (props.env_trace) {
        navigationLinksList.push(...trace)
    }

    if (props.env_nids) {
        navigationLinksList.push(...nids)
    }

    if (props.env_hids) {
        navigationLinksList.push(...hids)
    }

    if (props.env_hc) {
        navigationLinksList.push(...healthCheck)
    }

    if (props.env_soar) {
        navigationLinksList.push(...soar)
    }

    if (props.env_mm) {
        navigationLinksList.push(...mediaManagement)
    }

    if (props.env_tptf) {
        navigationLinksList.push(...TPThreadFeed)
    }

    if (props.env_sbs) {
        navigationLinksList.push(...sandBox)
    }

    if (props.env_ess) {
        navigationLinksList.push(...ess)
    }

    if (props.env_tps) {
        navigationLinksList.push(...tpSource)
    }

    if (props.xdr_live_map) {
        navigationLinksList.push(...liveMaps)
    }

    if (props.report) {
        navigationLinksList.push(...report)
    }

    if (props.administartion) {
        navigationLinksList.push(...administartion)
    }

    // if (props.env_wazuh) {
    //     navigationLinksList.push(...wazuh)
    // }

    return navigationLinksList
}

export default NavigationLinks