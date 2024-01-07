// =============================================================================================
//  File Name: pagePermissions.js
//  Description: Details of the page Permissions redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { token, setDefaultPath } from '@utils'
import axios from '@axios'

export const pagePermissions = () => {

    return dispatch => {

        axios.get(`/display-page-permissions`, { headers: { Authorization: token() } }).then(res => {
            dispatch({ type: "PAGES_PERMISSIONS_LOAD", payload: true })

            if (res.data.message_type === "success") {
                setDefaultPath({
                    default_page: res.data.data.default_page
                })

                dispatch({
                    type: "PAGES_PERMISSIONS",
                    payload: {
                        env_wazuh: res.data.data.env_wazuh,
                        env_trace: res.data.data.env_trace,
                        env_nids: res.data.data.env_nids,
                        env_hids: res.data.data.env_hids,
                        env_hc: res.data.data.env_hc,
                        env_mm: res.data.data.env_mm,
                        env_tptf: res.data.data.env_tptf,
                        env_sbs: res.data.data.env_sbs,
                        env_ess: res.data.data.env_ess,
                        env_tps: res.data.data.env_tps,
                        env_soar: res.data.data.env_soar,
                        xdr_live_map: res.data.data.xdr_live_map,
                        default_page: res.data.data.default_page
                    }
                })
            }
        })
            .catch(e => {
                console.warn(e.message)
            })
    }
}