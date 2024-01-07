// =============================================================================================
//  File Name: wsAction.js
//  Description: Details of the web socket redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

export const wsData = data => {
    return dispatch => {
        dispatch({ type: 'WS_DATA', payload: data })
    }
}