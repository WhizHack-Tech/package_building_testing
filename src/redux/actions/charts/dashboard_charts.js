// =============================================================================================
//  File Name: dashboard_charts.js
//  Description: Details of the dashboard charts redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { CHARTS, LOADER, DASHBOARD_FILTER_VALUE } from "../../constants/dashboard_charts_const"
import { token } from '@utils'
import axios from '@axios'

export const dashboar_charts = (data) => {
    return dispatch => {

        dispatch({type: LOADER, payload: true})

        axios.post("/date-filter", data,
          { headers: { Authorization: token()}})
          .then(res => {
                dispatch({type: LOADER, payload: false})
              dispatch({ type: CHARTS, payload: res.data})
          }).catch(err => {
            dispatch({type: LOADER, payload: false})
          })
    }
  }

export const dashboar_filter = (data) => {
    return dispatch => {
        dispatch({type: DASHBOARD_FILTER_VALUE, payload: data})
    }
  }