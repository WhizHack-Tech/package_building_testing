// =============================================================================================
//  File Name: lang_switch.js
//  Description: Details of the lang Switch redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { token } from '@utils'
import axios from '@axios'

export const langSwitch = () => {
    return dispatch => {
        axios.get(`/dashboard-lang`, { headers: { Authorization: token() } }).then(res => {
            if (res.data.message_type === "data_found") {
                dispatch({ type: "LANG_SWICH", payload: {langType: res.data.data.lang_type}})
            }
        })
    }
}