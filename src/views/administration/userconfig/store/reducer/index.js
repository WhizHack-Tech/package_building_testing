// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( Reducer ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** Initial State
const initialState = {  
  data: [],
  selectedUser: null,
  loader : true,
  error: null
}

const client_users = (state = initialState, action) => {
  switch (action.type) {
    case 'CLIENT_ALL_DATA':
      return { ...state, data: action.data, loader : false }    
    case 'SINGLE_USER':
      return { ...state, selectedUser: action.selectedUser, loader : false }
    case "CLIENT_ALL_DATA_LOAD":
      return { ...state, loader : false }  
    default:
      return { ...state }
  }
}
export default client_users
