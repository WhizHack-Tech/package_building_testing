// =============================================================================================
//  File Name: lang_switch.js
//  Description: Details of the language switch reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { getLang } from '@utils'
const initialState = {
  langType : getLang
}

const langSwitch = (state = initialState, action) => {
  switch (action.type) {
    case 'LANG_SWICH':
      return { ...state, langType: action.payload.langType }
    default:
      return state
  }
}

export default langSwitch
