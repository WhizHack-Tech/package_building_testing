// =============================================================================================
//  File Name: thirdParty.js
//  Description: Details of the thirdParty router component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { lazy } from 'react'

const ThirdParty = [  
  {
    path: '/third-party/trace',
    component: lazy(() => import('../../views/thirdParty/trace/')),
    exact: true
  },
  {
    path: '/third-party/wazuh',
    component: lazy(() => import('../../views/thirdParty/wazuh/')),
    exact: true
  },
  {
    path: '/third-party/wazuh/:id',
    component: lazy(() => import('../../views/thirdParty/wazuh/Views/index')),
    exact: true
  }
]

export default ThirdParty