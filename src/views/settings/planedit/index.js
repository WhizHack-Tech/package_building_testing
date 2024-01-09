// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Edit Plan ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { useState, Fragment } from 'react'
import BreadCrumbs from '@components/breadcrumbs'
// ** User Edit Components
import Planedit from './Planedit'
import DefalutPage from './DefalutPage'
import Lisence from './Lisences'
// ** Third Party Components
import { User, File, FileText } from 'react-feather'
import { Card, CardBody, Row, Col, Nav, NavItem, NavLink, TabContent, TabPane } from 'reactstrap'

// ** Styles
import '@styles/react/apps/app-users.scss'

const UserEdit = () => {

  // ** States & Vars
  const [activeTab, setActiveTab] = useState('1')
   
  // ** Function to toggle tabs
  const toggle = tab => setActiveTab(tab)
  return (
    <Fragment>
      <BreadCrumbs breadCrumbTitle='Plan Details'/>
    <Row className='app-user-edit'>
      <Col sm='12'>
        <Card lassName='plan-card border-primary'>
          <CardBody className='pt-2'>
            <Nav pills>
              <NavItem>
                <NavLink active={activeTab === '1'} onClick={() => toggle('1')}>
                  <User size={20} />
                  <span className='align-middle d-none d-sm-block'>Plan Details</span>
                </NavLink>
              </NavItem>
              <NavItem>
                <NavLink active={activeTab === '2'} onClick={() => toggle('2')} className='mr-2'>
                  <FileText size={20} />
                  <span className='align-middle d-none d-sm-block'>Products</span>
                </NavLink>
              </NavItem>
              <NavItem>
                <NavLink active={activeTab === '3'} onClick={() => toggle('3')} className='mr-2'>
                  <File size={20} />
                  <span className='align-middle d-none d-sm-block'>License</span>
                </NavLink>
              </NavItem>
            </Nav>
      
            <TabContent activeTab={activeTab}>
              <TabPane tabId='1'>
                <Planedit />
              </TabPane>
              <TabPane tabId='2'>
                <DefalutPage />
              </TabPane>
              <TabPane tabId='3'>
                <Lisence />
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
