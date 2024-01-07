// =============================================================================================
//  File Name: settings.js
//  Description: Details of the settings navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Edit, Settings } from 'react-feather'
export default [
  {
    id: 'settings',
    title: 'Settings',
    icon: <Settings />,
    children: [
      {
        id: 'editaccountsetting',
        title: 'Edit Account',
        icon: <Edit />,
        action: 'read',
        resource: 'ACL',
        navLink: '/settings/editaccount'
      }
    ]
  }
]
