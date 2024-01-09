// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Billing Edit ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { useState, Fragment } from 'react'
// ** User Edit Components
import BreadCrumbs from '@components/breadcrumbs'
import Billingedit from './Billingedit'
// ** Third Party Components
import { User } from 'react-feather'
import { Card, CardBody, Row, Col, Nav, NavItem, NavLink, TabContent, TabPane, Alert, Spinner } from 'reactstrap'

// ** Styles
import '@styles/react/apps/app-users.scss'

const UserEdit = () => {

  // ** States & Vars
  const [activeTab, setActiveTab] = useState('1')
   
  // ** Function to toggle tabs
  const toggle = tab => setActiveTab(tab)

  return (
    <Fragment>
    <BreadCrumbs breadCrumbTitle='Billing Details'/>
    <Row className='app-user-edit'>
      <Col sm='12'>
        <Card>
          <CardBody className='pt-2'>
            <Nav pills>
              <NavItem>
                <NavLink active={activeTab === '1'} onClick={() => toggle('1')}>
                  <User size={14} />
                  <span className='align-middle d-none d-sm-block'>Billing Details</span>
                </NavLink>
              </NavItem>
            </Nav>
            <TabContent activeTab={activeTab}>
              <TabPane tabId='1'>
                <Billingedit />
              </TabPane>
            </TabContent>
          </CardBody>
        </Card>
      </Col>
    </Row>
    </Fragment>
  )  
}
export default UserEdit
