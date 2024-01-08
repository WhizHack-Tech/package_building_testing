// ================================================================================================
//  File Name: Tabs.js
//  Description: Details of the Administration ( Add Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Nav, NavItem, NavLink } from 'reactstrap'
import { User } from 'react-feather'

const Tabs = ({ activeTab, toggleTab }) => {
  return (
    <Nav className='nav-left' pills vertical>
      <NavItem>
        <NavLink active={activeTab === '1'} onClick={() => toggleTab('1')}>
          <User size={18} className='mr-1' />
          <span className='font-weight-bold'>Basic Details</span>
        </NavLink>
      </NavItem>
    </Nav>
  )
}

export default Tabs
