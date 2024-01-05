// =============================================================================================
//  File Name: administartion.js
//  Description: Details of the administartion navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { Mail, UserPlus, Grid, Key, Tool, Gitlab, Users, Circle, Pocket } from 'react-feather'
export default [
  {
    header: 'Administration'
  },
  {
    id: 'Logs',
    title: 'Logs',
    icon: <Mail />,
    navLink: '/administration/logs'
  },
  {
    id: 'Userconfig',
    title: 'User Config',
    icon: <UserPlus />,
    navLink: '/administration/userconfig/list'
  },
  {
    id: 'integration',
    title: 'Integration',
    icon: <Grid size={20} />,
    children: [
      {
        id: 'apikey',
        title: 'Key Management',
        icon: <Key size={40} />,
        navLink: '/administration/Api-key'
      }
      // {
      //   id: 'wazuh',
      //   title: 'Wazuh',
      //   icon: <Gitlab size={20} />,
      //   externalLink: true,
      //   newTab: "_blank",
      //   navLink: 'https://the-aurors-office.whizhack-intranet.com/app/login'
      // }

    ]
  }
  // {
  //   id: 'shop',
  //   title: 'Shop',
  //   icon: <Mail />,
  //   navLink: '/administration/shop'
  // }
]
