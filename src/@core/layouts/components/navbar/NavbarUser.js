// =============================================================================================
//  File Name: NavbarUser.js
//  Description: Details of the Navbar User component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import IntlDropdown from './IntlDropdown'
import UserDropdown from './UserDropdown'
import { Sun, Moon } from 'react-feather'
import { NavItem, NavLink } from 'reactstrap'
import '@styles/react/apps/app-todo.scss'
const NavbarUser = props => {
   const { skin, setSkin } = props
  
  const ThemeToggler = () => {
    if (skin === 'dark') {
      return <Sun className='ficon' onClick={() => setSkin('light')} />
    } else {
      return <Moon className='ficon' onClick={() => setSkin('dark')} />
    }
  }

  return (
    <ul className='nav navbar-nav align-items-center ml-auto'>
      <IntlDropdown />
      <NavItem className='d-none d-lg-block'>
        <NavLink className='nav-link-style'>
          <ThemeToggler />
        </NavLink>
      </NavItem>
      <UserDropdown />
    </ul>
  )
}
export default NavbarUser
