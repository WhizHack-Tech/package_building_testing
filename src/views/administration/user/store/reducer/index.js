// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( Reducer ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** Initial State
/* const initialState = {
  allData: [],
  data: [],
  total: 1,
  params: {},
  selectedUser: null
} */

const initialState = {
  data: [],
  selectedUser:{
    message_type:null,
    data:{
      org_data: null,
      org_user_data:[]
    }
  },
  loading: false
}


const users = (state = initialState, action) => {
  switch (action.type) {
    case 'GET_ALL_DATA':
      return { ...state, data: action.data }
    case 'GET_DATA':
      return {
        ...state,
        data: action.data,
        total: action.totalPages,
        params: action.params
      }
    case 'GET_USER':
      return { ...state, selectedUser: action.selectedUser }
    case 'ADD_USER':
      return { ...state }
    case 'DELETE_USER':
      return { ...state }
    case 'USER_LOADING':
      return { ...state,  loading: action.playload }
    default:
      return { ...state }
  }
}
export default users
