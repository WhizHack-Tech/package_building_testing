// =============================================================================================
//  File Name: layout/index.js
//  Description: Details of the app layout reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** ThemeConfig Import
import themeConfig from '@configs/themeConfig'

// ** Returns Initial Menu Collapsed State
const initialMenuCollapsed = () => {
  const item = window.localStorage.getItem('menuCollapsed')
  //** Parse stored json or if none return initialValue
  return item ? JSON.parse(item) : themeConfig.layout.menu.isCollapsed
}

const initialContentWidth = () => {
  const item = window.localStorage.getItem('contentWidth')
  if (item === null) {
    return themeConfig.layout.contentWidth
  } else {
    return item
  }
}

const initialIsRTL = () => {
  const item = window.localStorage.getItem('isRTL')
  
  if (item === null) {
    return themeConfig.layout.isRTL
  } else {
    return JSON.parse(item)
  }
}

const initialMenuHidden = () => {
  const item = window.localStorage.getItem('menuHidden')
  if (item === null) {
    return themeConfig.layout.menu.isHidden
  } else {
    return JSON.parse(item)
  }
}

// ** Initial State
const initialState = {
  isRTL: initialIsRTL(),
  menuCollapsed: initialMenuCollapsed(),
  menuHidden: initialMenuHidden(),
  contentWidth: initialContentWidth()
}

const layoutReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'HANDLE_CONTENT_WIDTH':
      window.localStorage.setItem('contentWidth', action.value)
      return { ...state, contentWidth: action.value }
    case 'HANDLE_MENU_COLLAPSED':
      window.localStorage.setItem('menuCollapsed', action.value)
      return { ...state, menuCollapsed: action.value }
      case 'HANDLE_MENU_HIDDEN':
      window.localStorage.setItem('menuHidden', action.value)
      return { ...state, menuHidden: action.value }
    case 'HANDLE_RTL':
      window.localStorage.setItem('isRTL', action.value)
      return { ...state, isRTL: action.value }
    default:
      return state
  }
}

export default layoutReducer
