// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( Action ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import axios from "@axios"
// ** Utils
import { token } from '@utils'

// ** Get all Data
export const getAllData = () => {  
  return async dispatch => {

    dispatch({
      type: 'USER_LOADING',
      playload: false
    })

    await axios.get('/show-location-org/', { headers: { Authorization: token()} }).then(response => {
    // await axios.get('/org-location-json', { headers: { Authorization: token()} }).then(response => {
    
      dispatch({
        type: 'USER_LOADING',
        playload: true
      })

      if (response.data.message_type === 'data_found') {
        dispatch({
          type: 'GET_ALL_DATA',
          data: response.data.data
        })
      }


    }).catch(error => {
      dispatch({
        type: 'USER_LOADING',
        playload: false
      })
    })
  }
}

// ** Get data on page or row change
export const getData = params => {
  return async dispatch => {
    await axios.get(`/show-location-org/${params}`, { headers: { Authorization: token()} }).then(response => {
      dispatch({
        type: 'GET_DATA',
        data: response.data.users,
        totalPages: response.data.total,
        params
      })
    })
  }
}

// ** Get User
export const getUser = (id, activated_plan_id) => {
  return async dispatch => {
    await axios
      .get(`/show-location-org/${id}/${activated_plan_id}`, { headers: { Authorization: token()} })
      .then(response => {
        dispatch({
          type: 'GET_USER',
          selectedUser: response.data
        })
      })
      .catch(err => console.log(err))
  }
}

// ** Delete user
export const deleteUser = id => {
  return (dispatch, getState) => {
    axios
      .delete('/apps/users/delete/<uuid:pk>/', { id })
      .then(response => {
        dispatch({
          type: 'DELETE_USER'
        })
      })
      .then(() => {
        dispatch(getData(getState().users.params))
        dispatch(getAllData())
      })
  }
}
