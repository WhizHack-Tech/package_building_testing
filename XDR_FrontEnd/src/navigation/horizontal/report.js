// =============================================================================================
//  File Name: report.js
//  Description: Details of the report navbar object component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { FileText, Tool, Pocket, FilePlus } from 'react-feather'
export default [
  {
    id: 'reports',
    title: 'Insights',
    icon: <Tool />,
    children: [
      {
        id: 'reports',
        title: 'Static Reports',
        icon: <FileText />,
        action: 'read',
        resource: 'ADMIN',
        navLink: '/settings/Reports'
        },
        {
          id: 'reports_exports',
          title: 'Dynamic Reports',
          icon: <FilePlus />,
          action: 'read',
          resource: 'ADMIN',
          navLink: '/settings/reports-exports'
        }
        // {
        //   id: 'discover',
        //   title: 'Discover',
        //   icon: <Pocket />,
        //   action: 'read',
        //   resource: 'ADMIN',
        //   navLink: '/settings/discover'
        // }  

    ]
  }
]
