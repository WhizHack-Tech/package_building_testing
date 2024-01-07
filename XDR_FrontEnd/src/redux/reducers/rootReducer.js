// =============================================================================================
//  File Name: rootReducer.js
//  Description: Details of the root Reducers component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Redux Imports
import { combineReducers } from 'redux'

// ** Reducers Imports
import auth from './auth'
import navbar from './navbar'
import layout from './layout'
import users from '@src/views/administration/userconfig/store/reducer'
import dashboard_charts from "./charts/dashboard_chart"
import attack_evnets_charts from "./charts/attack-envents-reducer"
import tables_charts from "./charts/tables_chart"
import ws_reducer from './ws/wsReducer'
import test_page from "./charts/test-page"
import langSwitch from './layout/lang_switch'
import pagesPermissions from './layout/pagesPermissions'
import dashboard_chart from '../../views/nids/store/dashboard_chart'
import incident_charts from '../../views/hids/store/incident_charts'
import global_charts from '../../views/trace/global_threat_feed/store/global_charts'
import reports_exports from '../../views/settings/reports_exports/store/reducer'
import health_sensor from '../../views/healthCheck/store/health_sensor'
const rootReducer = combineReducers({
  auth,
  navbar,
  layout,
  users,
  dashboard_charts,
  attack_evnets_charts,
  tables_charts,
  ws_reducer,
  test_page,
  langSwitch,
  pagesPermissions,
  dashboard_chart,
  incident_charts,
  reports_exports,
  global_charts,
  health_sensor
})

export default rootReducer
