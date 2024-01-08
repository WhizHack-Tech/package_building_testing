// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Action ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import axios from '@axios'
import { token } from '@utils'

// ** Get all Data
export const billing_details = () => {
  return async dispatch => {
    await axios.get('/billinglist/', { headers: { Authorization: token()} }).then(response => {
      if (response.data.message_type === 'data_found') {
        dispatch({
          type: 'Billing_ALL_DATA',
          data: response.data.data
        })
      }
    })
  }
}
