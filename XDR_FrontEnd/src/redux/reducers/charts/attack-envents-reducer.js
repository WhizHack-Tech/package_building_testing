// =============================================================================================
//  File Name: attack-envents-reducer.js
//  Description: Details of the attack-envents-reducer reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { CHARTS_EVENT, LOADER_EVNET, ATTACK_FILTER_VALUE } from "../../constants/dashboard_charts_const"

const initialState = {
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
    charts: {},
    loadding:false
  }
 
  const attack_evnets_charts = (state = initialState, action) => {
    switch (action.type) {
      case CHARTS_EVENT:
         return { ...state, charts: action.payload}
      break
      case LOADER_EVNET:
        return {...state, loadding: action.payload}
      break
      case ATTACK_FILTER_VALUE:
        return {...state, filterValue: action.payload}
      default:
        return state
    }
  }
 
  export default attack_evnets_charts