// ================================================================================================
//  File Name: index.js
//  Description: User Config Details(reducer).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
const initialState = {
  data: [],
  selectedUser:null,
  loading : true
}


const users = (state = initialState, action) => {
  switch (action.type) {
    case 'GET_ALL_DATA':
      return { ...state, data: action.data, loading : false }
    case 'GET_DATA':
      return {
        ...state,
        data: action.data,
        total: action.totalPages,
        params: action.params
      }
    case 'GET_USER':
      return { ...state, selectedUser: action.selectedUser, loading : false }
      case "GET_ALL_DATA_LOAD":
      return { ...state, loading : false } 
    case 'DELETE_USER':
      return { ...state }
    default:
      return { ...state }
  }
}
export default users
