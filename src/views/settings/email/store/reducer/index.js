// ** Initial State
const initialState = {  
  data: [],
  selectedUser: null,
  loader : true
}

const email_details = (state = initialState, action) => {
  switch (action.type) {
    case 'Email_ALL_DATA':
      return { ...state, data: action.data, loader : false } 
    default:
      return { ...state }
  }
}
export default email_details
