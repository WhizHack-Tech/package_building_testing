// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( Action ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import axios from '@axios'
import { token } from '@utils'

// ** Get all Data
export const clientAllData = () => {
  return async dispatch => {
    await axios.get('/displayuser/', { headers: { Authorization: token()} }).then(response => {
      dispatch({
        type: 'CLIENT_ALL_DATA',
        data: response.data
      })
    }).catch(err => {
      dispatch({
        type: 'CLIENT_ALL_DATA_LOAD'
      })
    })
  }
}

// ** Get User
export const getUser = id => {
  return async dispatch => {
    await axios
      .get(`/displayuser/${id}/`, { headers: { Authorization: token()} })
      .then(response => {
        dispatch({
          type: 'GET_USER',
          selectedUser: response.data
        })
      })
      .catch(err => console.log(err))
  }
}

// ** Get Single User
export const singleClient = id => {
  return async dispatch => {
    await axios
    .get(`/displayuser/${id}/`, { headers: { Authorization: token()} })
      .then(response => {
        dispatch({
          type: 'SINGLE_USER',
          selectedUser: response.data
        })
      })
      .catch(err => console.log(err))
  }
}
