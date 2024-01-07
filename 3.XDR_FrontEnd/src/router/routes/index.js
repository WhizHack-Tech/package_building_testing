// =============================================================================================
//  File Name: routes/index.js
//  Description: Details of the index router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { getDefaultPath } from '@utils'

import AuthRoutes from './Auth'
// import DashboardRoutes from './Dashboard'
import AdministrationRoutes from './Administration'
import SettingsRoutes from './Settings'
import ThirdParty from './thirdParty'

import Hids from './hids'
import Nids from './nids'
import Trace from './trace'
import Wazuh from './wazuh'
import LiveMaps from './liveMaps'
import HealthCheck from './healthCheck'
import Soar from './soar'
import mediaManagement from './mediaManagement'
import TPThreadFeed from './TPThreadFeed'
import sandBox from './sandBox'
import ess from './ess'
import tpSource from './tpSource'

// ** Document title
const TemplateTitle = '%s - XDR Client'

// ** Default Route
const DefaultRoute = getDefaultPath('/')


// ** Merge Routes
const Routes = [
  ...AuthRoutes,
  // ...DashboardRoutes,
  ...AdministrationRoutes,
  ...SettingsRoutes,
  ...ThirdParty,
  ...Hids,
  ...Nids,
  ...Trace,
  ...Wazuh,
  ...LiveMaps,
  ...HealthCheck,
  ...Soar,
  ...mediaManagement,
  ...TPThreadFeed,
  ...sandBox,
  ...ess,
  ...tpSource
]

export { DefaultRoute, TemplateTitle, Routes }
