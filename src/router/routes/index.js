 // ================================================================================================
//  File Name: index.js
//  Description: Details Pages of the index ( Routes ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import AuthRoutes from './Auth'
import AdministrationRoutes from './Administration'
import DashboardRoutes from './Dashboard'
import FaqRoutes from './Faq'
import SettingsRoutes from './Settings'
// ** Document title
const TemplateTitle = '%s - XDR ZeroHack Master'

// ** Default Route
const DefaultRoute = '/dashboard/agent'


// ** Merge Routes
const Routes = [
  ...AuthRoutes,
  ...DashboardRoutes,
  ...AdministrationRoutes,
  ...FaqRoutes,
  ...SettingsRoutes
]

export { DefaultRoute, TemplateTitle, Routes }
