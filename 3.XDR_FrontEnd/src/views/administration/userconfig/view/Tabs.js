
// ================================================================================================
//  File Name:  Tba.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
// ** React Imports
import { Fragment } from 'react'

// ** Reactstrap Imports
import { Nav, NavItem, NavLink, TabContent, TabPane, Card, CardBody } from 'reactstrap'

// ** Icons Imports
import { User, Lock, Bookmark } from 'react-feather'

import PersonalInformation from './PersonalInformation'
import Logs from './Logs'
import { useTranslation } from 'react-i18next'

const UserTabs = ({ active, toggleTab, selectedUser }) => {
  const {t} = useTranslation()
  return (
    <Fragment>
      <Card>
      <CardBody>
      <Nav pills className='mb-2'>
        <NavItem>
          <NavLink active={active === '1'} onClick={() => toggleTab('1')}>
            <User className='font-medium-3 me-50' />
            <span className='fw-bold'>{t('Personal Information')}</span>
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink active={active === '2'} onClick={() => toggleTab('2')}>
            <Bookmark className='font-medium-3 me-50' />
            <span className='fw-bold'>{t('Logs')}</span>
          </NavLink>
        </NavItem>
      </Nav>
      <TabContent activeTab={active}>
        <TabPane tabId='1'>
          <PersonalInformation selectedUser={selectedUser} />
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