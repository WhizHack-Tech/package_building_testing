 // ================================================================================================
//  File Name: index.js
//  Description: Details Pages of the Auth ( Redux ( Reducer )).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
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
    default:
      return state
  }
}

export default authReducer
