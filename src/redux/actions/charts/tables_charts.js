// =============================================================================================
//  File Name: tables_charts.js
//  Description: Details of the tables charts redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { TABLE_EVENT, LOADER_TABLE, TABLE_FILTER_VALUE } from "../../constants/dashboard_charts_const"
import { token } from '@utils'
import axios from '@axios'

export const tables_charts = (data) => {
    return dispatch => {

        dispatch({type: LOADER_TABLE, payload: true})

        axios.post("/charts-intelligence", data,
          { headers: { Authorization: token()}})
          .then(res => {
                dispatch({type: LOADER_TABLE, payload: false})
              dispatch({ type: TABLE_EVENT, payload: res.data})
          }).catch(err => {
            dispatch({type: LOADER_TABLE, payload: false})
          })
    }
  }

  export const table_filter = (data) => {
    return dispatch => {
        dispatch({type: TABLE_FILTER_VALUE, payload: data})
    }
  }