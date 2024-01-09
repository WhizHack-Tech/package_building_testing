 // ================================================================================================
//  File Name: rootReducer.js
//  Description: Details Pages of the RootReducer ( Redux ( Reducer )).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Redux Imports
import { combineReducers } from 'redux'

// ** Reducers Imports
import auth from './auth'
import navbar from './navbar'
import layout from './layout'
import users from '@src/views/administration/user/store/reducer'
import client_users from '@src/views/administration/userconfig/store/reducer'
import billing_details from '@src/views/settings/billing/store/reducer'
import plan_details from '@src/views/settings/plans/store/reducer'
import email_details from '@src/views/settings/email/store/reducer'
import application_details from '@src/views/settings/application/store/reducer'

const rootReducer = combineReducers({
  auth,
  navbar,
  layout,
  users,
  client_users,
  billing_details,
  plan_details,
  email_details,
  application_details
})

export default rootReducer
