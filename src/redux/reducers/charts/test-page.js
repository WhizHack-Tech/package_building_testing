// =============================================================================================
//  File Name: test-page.js
//  Description: Details of the filter dashboard reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { TEST_CHARTS_FILTER, TEST_LOADING, TEST_FILTER_VALUE } from "../../constants/dashboard_charts_const"

const initialState = {
    filterValue : {
      defaultVals: {
        platformVal: [],
        accuracyVal: [],
        platformSetVal: [],
        accuracySetVal: []
      },
      platform: [],
      accuracy: [],
      start_date:"",
      end_date:""
    },
    charts: {},
    loadding:false
  }
 
  const test_page = (state = initialState, action) => {
    switch (action.type) {
      case TEST_CHARTS_FILTER:
         return { ...state, charts: action.payload}
      break
      case TEST_LOADING:
        return {...state, loadding: action.payload}
      break
      case TEST_FILTER_VALUE:
        return {...state, filterValue: action.payload}
      default:
        return state
    }
  }
 
  export default test_page