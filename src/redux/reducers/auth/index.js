// =============================================================================================
//  File Name: auth/index.js
//  Description: Details of the auth reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// **  Initial State
const initialState = {
  userData: {}
}

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'LOGIN':
      return { ...state, userData: action.data }
    case 'LOGOUT':
      return { ...state, userData: {} }
    case 'PROFILE_UPDATE':
    return { ...state, userData: action.data }
    default:
      return state
  }
}

export default authReducer
