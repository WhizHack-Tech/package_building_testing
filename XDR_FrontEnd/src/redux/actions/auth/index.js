// =============================================================================================
//  File Name: auth/index.js
//  Description: Details of the auth redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { wsDis } from "../../../ws_con" 
// ** Handle User Login
export const handleLogin = data => {
  return dispatch => {
    dispatch({ type: 'LOGIN', data })

    // ** Add to user to localStorage
    localStorage.setItem('clientData', JSON.stringify(data))
  }
}

// ** Handle User Logout
export const handleLogout = () => {
  return dispatch => {
    wsDis()
    dispatch({ type: 'LOGOUT' }) 
    // ** Remove user from localStorage
    localStorage.removeItem('clientData')
  }
}


export const updateProfile = (data) => {
  return dispatch => {
    dispatch({ type: 'PROFILE_UPDATE', data})
  }
}
