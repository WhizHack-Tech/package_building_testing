 // ================================================================================================
//  File Name: administration.js
//  Description: Details Pages of the Navigtion ( Vertical ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Mail, UserPlus, CheckSquare, Tool, Settings, Users, Circle, ShoppingCart, Package, User } from 'react-feather'

export default [
  {
    header: 'Administration',
    action: 'read',
    resource: 'ADMIN'
  },
  {
    id: 'users',
    title: 'Organization Settings',
    icon: <User size={20} />,
    navLink: '/administration/user/list',
    action: 'read',
    resource: 'ADMIN'     
  },
  {
    id: 'userconfig',
    title: 'Client User Config',
    icon: <Users size={20} />,
    navLink: '/administration/userconfig/list',
    action: 'read',
    resource: 'ADMIN'        
  },     
  // {
  //   id: 'roles',
  //   title: 'Roles',
  //   icon: <UserPlus />,
  //   navLink: '/administration/roles',
  //   action: 'read',
  //   resource: 'ADMIN'
  // },
  {
    id: 'logs',
    title: 'Logs',
    icon: <UserPlus />,
    navLink: '/administration/logs',
    action: 'read',
    resource: 'ADMIN'
  } 
]
