// ================================================================================================
//  File Name: Tabs.js
//  Description: Details of the Administration ( View User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { Fragment } from 'react'

// ** Reactstrap Imports
import { Nav, NavItem, NavLink, TabContent, TabPane, Card, CardBody } from 'reactstrap'

// ** Icons Imports
import { User, Lock, Bookmark } from 'react-feather'

// ** User Components
import Logs from './Logs'
import PersonalInformation from './PersonalInformation'

const UserTabs = ({ active, toggleTab }) => {
  return (
    <Fragment>
      <Card>
      <CardBody>
      <Nav pills className='mb-2'>
        <NavItem>
          <NavLink active={active === '1'} onClick={() => toggleTab('1')}>
            <User className='font-medium-3 me-50' />
            <span className='fw-bold'>Personal Information</span>
          </NavLink>
        </NavItem>
        {/* <NavItem>
          <NavLink active={active === '2'} onClick={() => toggleTab('2')}>
            <Lock className='font-medium-3 me-50' />
            <span className='fw-bold'>Security</span>
          </NavLink>
        </NavItem> */}
        <NavItem>
          <NavLink active={active === '2'} onClick={() => toggleTab('2')}>
            <Bookmark className='font-medium-3 me-50' />
            <span className='fw-bold'>Logs</span>
          </NavLink>
        </NavItem>
      </Nav>
      <TabContent activeTab={active}>
        <TabPane tabId='1'>
          <PersonalInformation />
        </TabPane>
        <TabPane tabId='2'>
          <Logs />
        </TabPane>
      </TabContent>
      </CardBody>
      </Card>
    </Fragment>
  )
}
export default UserTabs
