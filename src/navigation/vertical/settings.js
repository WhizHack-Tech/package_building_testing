 // ================================================================================================
//  File Name: setting.js
//  Description: Details Pages of the Navigtion ( Vertical ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { BookOpen, Circle, Settings, AlignJustify, Mail } from 'react-feather'

export default [
  {
    id: 'settings',
    title: 'Settings',
    icon: <Settings size={20} />, 
    children: [
      {
        id: 'plan2',
        title: 'Plan',
        icon: <BookOpen />,
        navLink: '/settings/plan2'
      },
      // {
      //   id: 'plan',
      //   title: 'Plan',
      //   icon: <AlignJustify size={12} />,
      //   navLink: '/settings/plans'
      // },
      {
        id: 'billing',
        title: 'Billing',
        icon: <Circle size={12} />,
        navLink: '/settings/billing'
      }
      // {
      //   id: 'email',
      //   title: 'Email Config',
      //   icon: <Mail size={12} />,
      //   navLink: '/settings/email'
      // },
      // {
      //   id: 'application',
      //   title: 'Application',
      //   icon: <BookOpen />,
      //   navLink: '/settings/application'
      // }
    ]
  }
]