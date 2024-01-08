 // ================================================================================================
//  File Name: index.js
//  Description: Details Pages of the Navigtion ( Vertical ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Navigation sections imports


import administration from './administration'
import dashboard from './dashboard'
import settings from './settings'
// import faq from './faq'
// ** Merge & Export

export default [...dashboard, ...administration, ...settings]