// ================================================================================================
//  File Name: Config.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useState, useEffect } from 'react'
import Tabs2 from './Tabs2'
import Email from './Email'
// import Environment from './Environment'
import Notification from './Notification'
import Dashboard from './Dashboard'
// import Azure from './Azure'
import { Row, Col, TabContent, TabPane, Card, CardBody } from 'reactstrap'

import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/pages/page-account-settings.scss'


const AccountSettings = () => {
  const [activeTab, setActiveTab] = useState('1')

  const toggleTab = tab => {
    setActiveTab(tab)
  }
  return (
    <Fragment>
      <Col>
        <Tabs2 activeTab={activeTab} toggleTab={toggleTab} />
      </Col>
      <Row>
        <Col md='12'>
          <Card>
            <CardBody>
              <TabContent activeTab={activeTab}>
                <TabPane tabId='1'>
                  <Email />
                </TabPane>
                <TabPane tabId='2'>
                  <Notification />
                </TabPane>
                <TabPane tabId='3'>
                  <Dashboard />
                </TabPane>
                {/* <TabPane tabId='4'>
                    <Environment />
                  </TabPane> */}
              </TabContent>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Fragment>
  )
}

export default AccountSettings
