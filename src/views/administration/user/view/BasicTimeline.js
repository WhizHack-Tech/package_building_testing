// ================================================================================================
//  File Name: BasicTimeline.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import { Fragment, useState, useEffect } from 'react'
import Tabs from './Tabs'
import Email from './Email'
import Dashboard from './Dashboard'
import Pages from './Pages'
import Lisences from './Linsence'
import GroupMailConfig from "./groupMailConfig"
import PlanDetails from './PlanEdit'
// import Azure from './Azure'
import { Row, Col, TabContent, TabPane, Card, CardBody } from 'reactstrap'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/pages/page-account-settings.scss'
// import Environment from './Environment'
import Notification from './Notification'

const AccountSettings = () => {
  const [activeTab, setActiveTab] = useState('1')

  const toggleTab = tab => {
    setActiveTab(tab)
  }
  return (
    <Fragment>
      <Tabs activeTab={activeTab} toggleTab={toggleTab} />
      <TabContent activeTab={activeTab}>
        <TabPane tabId='1'>
          <Email />
        </TabPane>
        <TabPane tabId='2'>
          <Dashboard />
        </TabPane>
        <TabPane tabId='3'>
          <Notification />
        </TabPane>
        <TabPane tabId='4'>
          <Pages />
        </TabPane>
        <TabPane tabId='5'>
          <Lisences />
        </TabPane>
        <TabPane tabId='6'>
          <GroupMailConfig />
        </TabPane>
        <TabPane tabId='7'>
          <PlanDetails />
        </TabPane>
      </TabContent>
    </Fragment>
  )
}

export default AccountSettings
