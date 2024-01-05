// =============================================================================================
//  File Name: wsReducer.js
//  Description: Details of the web socket reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

const initialState = {
    notificationData : {
        notificationRes: [],
        notificationEmail: []
    }
}

const ws_reducer = (state = initialState, action) => {
    switch (action.type) {
        case 'WS_DATA':
            return { ...state, notificationData: action.payload }
        default:
            return state
    }
}

export default ws_reducer
