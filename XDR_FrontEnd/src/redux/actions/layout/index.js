// =============================================================================================
//  File Name: layout/index.js
//  Description: Details of the app layout redux component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Handles Layout Content Width (full / boxed)
export const handleContentWidth = value => dispatch => dispatch({ type: 'HANDLE_CONTENT_WIDTH', value })

// ** Handles Menu Collapsed State (Bool)
export const handleMenuCollapsed = value => dispatch => dispatch({ type: 'HANDLE_MENU_COLLAPSED', value })

// ** Handles Menu Hidden State (Bool)
export const handleMenuHidden = value => dispatch => dispatch({ type: 'HANDLE_MENU_HIDDEN', value })

// ** Handles RTL (Bool)
export const handleRTL = value => dispatch => dispatch({ type: 'HANDLE_RTL', value })
