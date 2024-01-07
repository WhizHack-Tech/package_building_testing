// ================================================================================================
//  File Name: Tabspages.js
//  Description: Details of the NIDS Incidents ( Tabs Pages )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useState, useEffect } from 'react'
import Attack from './AttackedHostDetails'
import { useTranslation } from 'react-i18next'
import Tabs from './Tabs'
import Tabs1 from './IDS_Tab'
import ML_DL from './ML_DL_Tab'
import { Row, Col, TabContent, TabPane, Card, CardBody } from 'reactstrap'

const AccountSettings = () => {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState('1')

  const toggleTab = tab => {
    setActiveTab(tab)
  }
  return (
    <Fragment>
      <Col>
        <Tabs activeTab={activeTab} toggleTab={toggleTab} />
      </Col>
      <Row>
        <Col md='12'>
              <TabContent activeTab={activeTab}>
                <TabPane tabId='1'>
                  <Tabs1 />
                </TabPane>
                <TabPane tabId='2'>
                  <ML_DL />
                </TabPane>
              </TabContent>
        </Col>
      </Row>
    </Fragment>
  )
}

export default AccountSettings
