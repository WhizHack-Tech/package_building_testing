// =============================================================================================
//  File Name: tables_chart.js
//  Description: Details of the tables chart reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { TABLE_EVENT, LOADER_TABLE, TABLE_FILTER_VALUE } from "../../constants/dashboard_charts_const"

const initialState = {
    charts: {},
    filterValue : {
      defaultVals: {
        platformVal: [],
        severityVal: [],
        platformSetVal: [],
        severitySetVal: []
      },
      platform:[],
      threat_severity:[],
      start_date:"",
      end_date:""
    },
    loadding:false
  }
 
  const tables_chart = (state = initialState, action) => {
    switch (action.type) {
      case TABLE_EVENT:
         return { ...state, charts: action.payload}
      break
      case LOADER_TABLE:
        return {...state, loadding: action.payload}
        case TABLE_FILTER_VALUE:
        return {...state, filterValue: action.payload}
      break
      default:
        return state
    }
  }
 
  export default tables_chart