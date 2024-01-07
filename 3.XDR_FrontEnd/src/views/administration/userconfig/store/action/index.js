// ================================================================================================
//  File Name: index.js
//  Description: User Config Details (Redux).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
import axios from "@axios"
// ** Utils
import { token } from '@utils'

// ** Get all Data
export const getAllData = () => {
  return async dispatch => {
    await axios.get('/users/list/all-data').then(response => {
      dispatch({
        type: 'GET_ALL_DATA',
        data: response.data
      })
    })
  }
}

// ** Get data on page or row change
export const getData = params => {
  return async dispatch => {
    await axios.get('/users/list/data', params).then(response => {
      dispatch({
        type: 'GET_DATA',
        data: response.data.users,
        totalPages: response.data.total,
        params
      })
    })
  }
}

export const getUser = id => {
  return async dispatch => {
    await axios
      .get(`/sub-clients?id=${id}`, { headers: { Authorization: token()} })
      .then(response => {
        dispatch({
          type: 'GET_USER',
          selectedUser: response.data
        })
      })
      .catch(err => console.log(err))
  }
}
