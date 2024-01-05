// =============================================================================================
//  File Name: settings.js
//  Description: Details of the settings navebar component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Home, Circle, Edit, CheckSquare, Pocket } from 'react-feather'

export default [
  {
    title: 'Settings',
    action: 'read',
    resource: 'ACL'
  },
  
      {
        id: 'editaccountsetting',
        title: 'Edit Account',
        icon: <Edit />,
        action: 'read',
        resource: 'ACL',
        navLink: '/settings/editaccount'
      }
    
]
