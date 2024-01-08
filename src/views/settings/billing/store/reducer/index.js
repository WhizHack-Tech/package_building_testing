// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Reducer ).
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

const billing_details = (state = initialState, action) => {
  switch (action.type) {
    case 'Billing_ALL_DATA':
      return { ...state, data: action.data, loader : false } 
    default:
      return { ...state }
  }
}
export default billing_details
