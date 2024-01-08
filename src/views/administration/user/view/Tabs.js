// ================================================================================================
//  File Name: Tabs.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import { Nav, NavItem, NavLink, CardBody } from 'reactstrap'
import { User, Lock, Info, Link, Bell } from 'react-feather'
import { FormattedMessage } from 'react-intl'
const Tabs = ({ activeTab, toggleTab }) => {
  return (
    <Nav className='nav-inline' pills>
      <NavItem>
        <NavLink active={activeTab === '1'} onClick={() => toggleTab('1')} className='mr-3'>
          <span className='font-weight-bold'><FormattedMessage id='Email Config' /></span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '2'} onClick={() => toggleTab('2')} className='mr-3'>
          <span className='font-weight-bold'><FormattedMessage id='Dashboard Config' /></span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '3'} onClick={() => toggleTab('3')} className='mr-3'>
          <span className='font-weight-bold'><FormattedMessage id='Notification Config' /></span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '4'} onClick={() => toggleTab('4')} className='mr-3'>
          <span className='font-weight-bold'>Products</span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '5'} onClick={() => toggleTab('5')} className='mr-3'>
          <span className='font-weight-bold'>License Management</span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '6'} onClick={() => toggleTab('6')} className='mr-3'>
          <span className='font-weight-bold'>Group Mail Notification</span>
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink active={activeTab === '7'} onClick={() => toggleTab('7')} className='mr-2'>
          <span className='font-weight-bold'>Upgrade Plan</span>
        </NavLink>
      </NavItem>
    </Nav>

  )
}

export default Tabs
