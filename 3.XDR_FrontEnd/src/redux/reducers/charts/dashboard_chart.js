// =============================================================================================
//  File Name: dashboard_chart.js
//  Description: Details of the dashboard chart reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { CHARTS, LOADER, DASHBOARD_FILTER_VALUE } from "../../constants/dashboard_charts_const"

const initialState = {
  charts: {},
  filterValue: {
    defaultVals: {
      platformVal: [],
      severityVal: [],
      platformSetVal: [],
      severitySetVal: []
    },
    platform: [],
    threat_severity: [],
    start_date: "",
    end_date: ""
  },
  loadding: false
}

const dashboard_charts = (state = initialState, action) => {
  switch (action.type) {
    case CHARTS:
      return { ...state, charts: action.payload }
      break
    case LOADER:
      return { ...state, loadding: action.payload }
      break
    case DASHBOARD_FILTER_VALUE:
      return { ...state, filterValue: action.payload }
      break
    default:
      return state
  }
}

export default dashboard_charts