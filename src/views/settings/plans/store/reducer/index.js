// ** Initial State
const initialState = {  
  data: [],
  selectedUser: null,
  loader : false
}

const plan_details = (state = initialState, action) => {
  switch (action.type) {
    case 'Plan_ALL_DATA':
      return { ...state, data: action.data, loader : true }
    default:
      return { ...state }
  }
}
export default plan_details
