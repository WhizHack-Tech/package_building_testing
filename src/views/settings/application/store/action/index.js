// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Application ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import axios from '@axios'
import { token } from '@utils'

// ** Get all Data
export const application_details = () => {
  return async dispatch => {
    await axios.get('/application-views/', { headers: { Authorization: token()} }).then(response => {
      dispatch({
        type: 'APPLICATION_ALL_DATA',
        data: response.data
      })
    })
  }
}
