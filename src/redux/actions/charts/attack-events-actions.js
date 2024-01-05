// =============================================================================================
//  File Name: attack-events-actions.js
//  Description: Details of the attack-events-actions redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { CHARTS_EVENT, LOADER_EVNET, ATTACK_FILTER_VALUE } from "../../constants/dashboard_charts_const"
import { token } from '@utils'
import axios from '@axios'

export const attack_events_charts = (data) => {
    return dispatch => {

        dispatch({type: LOADER_EVNET, payload: true})

        axios.post("/charts-attack-events", data,
          { headers: { Authorization: token()}})
          .then(res => {
                dispatch({type: LOADER_EVNET, payload: false})
              dispatch({ type: CHARTS_EVENT, payload: res.data})
          }).catch(err => {
            dispatch({type: LOADER_EVNET, payload: false})
          })
    }
  }

  export const attack_filter = (data) => {
    return dispatch => {
        dispatch({type: ATTACK_FILTER_VALUE, payload: data})
    }
  }