 // ================================================================================================
//  File Name: faq.js
//  Description: Details Pages of the Navigtion ( Vertical ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { MessageSquare, MessageCircle, Plus, Circle, User } from 'react-feather'

export default [
  {
    id: 'faq',
    title: 'FAQ',
    icon: <MessageSquare size={15} />,
    badge: 'light-warning',
    children: [
      {
        id: 'addfaq',
        title: 'Add',
        icon: <Plus size={15} />,
        navLink: '/faq/add'
      },
      {
        id: 'faq',
        title: 'FAQ`s',
        icon: <MessageCircle size={15} />,
        navLink: '/faq/faq'
      }
    ]
  }
  // {
  //   id: 'users',
  //   title: 'User',
  //   icon: <User size={20} />,
  //   children: [
  //     {
  //       id: 'list',
  //       title: 'List',
  //       icon: <Circle size={12} />,
  //       navLink: '/faq/user/list'
  //     },
  //     {
  //       id: 'view',
  //       title: 'View',
  //       icon: <Circle size={12} />,
  //       navLink: '/faq/user/view'
  //     },
  //     {
  //       id: 'edit',
  //       title: 'Edit',
  //       icon: <Circle size={12} />,
  //       navLink: '/faq/user/edit'
  //     }
  //   ]
  // }
]
