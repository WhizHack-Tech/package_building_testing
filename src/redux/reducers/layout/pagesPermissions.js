// =============================================================================================
//  File Name: pagesPermissions.js
//  Description: Details of the pages Permissions reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

const initialState = {
    env_wazuh: false,
    env_trace: false,
    env_nids: false,
    env_hids: false,
    env_hc: false,
    env_mm: false,
    env_tptf: false,
    env_sbs: false,
    env_ess: false,
    env_tps: false,
    env_soar: false,
    xdr_live_map: false,
    default_page: null,
    loading: false
}

const pagesPermissions = (state = initialState, action) => {
    switch (action.type) {
        case 'PAGES_PERMISSIONS':
            return {
                ...state,
                env_wazuh: action.payload.env_wazuh,
                env_trace: action.payload.env_trace,
                env_nids: action.payload.env_nids,
                env_hids: action.payload.env_hids,
                env_hc: action.payload.env_hc,
                env_mm: action.payload.env_mm,
                env_tptf: action.payload.env_tptf,
                env_sbs: action.payload.env_sbs,
                env_ess: action.payload.env_ess,
                env_tps: action.payload.env_tps,
                env_soar: action.payload.env_soar,
                xdr_live_map: action.payload.xdr_live_map,
                default_page: action.payload.default_page
            }
            break
        case "PAGES_PERMISSIONS_LOAD":
            return { ...state, loading: action.payload }
            break

        default:
            return state
    }
}

export default pagesPermissions
