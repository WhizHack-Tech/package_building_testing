// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Application ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** Initial State
const initialState = {  
  data: [],
  selectedUser: null,
  loader : true
}

const application_details = (state = initialState, action) => {
  switch (action.type) {
    case 'APPLICATION_ALL_DATA':
      return { ...state, data: action.data, loader : false } 
    default:
      return { ...state }
  }
}
export default application_details
