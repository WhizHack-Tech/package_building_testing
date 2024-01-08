// ================================================================================================
//  File Name: index.js
//  Description: Details Pages of the Navigtion ( Horizontal ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Navigation sections imports
import administration from './administration'
import dashboard from './dashboard'
import settings from './settings'
// ** Merge & Export

export default [...dashboard, ...administration, ...settings]