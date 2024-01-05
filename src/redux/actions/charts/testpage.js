// =============================================================================================
//  File Name: testpage.js
//  Description: Details of the filter dashboard redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { TEST_CHARTS_FILTER, TEST_LOADING, TEST_FILTER_VALUE } from "../../constants/dashboard_charts_const"
import { token } from '@utils'
import axios from '@axios'

export const test_page = (data) => {
    return dispatch => {

        dispatch({type: TEST_LOADING, payload: true})

        axios.post("/api", data,
          { headers: { Authorization: token()}})
          .then(res => {
                dispatch({type: TEST_LOADING, payload: false})
              dispatch({ type: TEST_CHARTS_FILTER, payload: res.data})
          }).catch(err => {
            dispatch({type: TEST_LOADING, payload: false})
          })
    }
  }

  export const test_filter = (data) => {
    return dispatch => {
        dispatch({type: TEST_FILTER_VALUE, payload: data})
    }
  }