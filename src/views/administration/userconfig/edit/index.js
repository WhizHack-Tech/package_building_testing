// ================================================================================================
//  File Name:  index.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
// ** React Imports
import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

// ** User Edit Components
import AccountTab from './Account'

// ** Store & Actions
import { getUser } from '../store/action'
import { useSelector, useDispatch } from 'react-redux'

// ** Third Party Components
import { User, Info, Share2 } from 'react-feather'
import { Card, CardBody, Row, Col, Nav, NavItem, NavLink, TabContent, TabPane, Alert } from 'reactstrap'

// ** Styles
import '@styles/react/apps/app-users.scss'

const UserEdit = () => {
  // ** States & Vars
  const [activeTab, setActiveTab] = useState('1'),
    store = useSelector(state => state.users),
    dispatch = useDispatch(),
    { id } = useParams()

  // ** Function to toggle tabs
  const toggle = tab => setActiveTab(tab)

  // ** Function to get user on mount
  useEffect(() => {
    dispatch(getUser(id))
  }, [dispatch])

  return (
    <Row className='app-user-edit'>
      <Col sm='12'>
        <Card>
          <CardBody className='pt-2'>
            <Nav pills>
              <NavItem>
                <NavLink active={activeTab === '1'} onClick={() => toggle('1')}>
                  <User size={14} />
                  <span className='align-middle d-none d-sm-block'>Account</span>
                </NavLink>
              </NavItem>
              {/* <NavItem>
                <NavLink active={activeTab === '2'} onClick={() => toggle('2')}>
                  <Info size={14} />
                  <span className='align-middle d-none d-sm-block'>Information</span>
                </NavLink>
              </NavItem> */}
              {/*<NavItem>
                <NavLink active={activeTab === '3'} onClick={() => toggle('3')}>
                  <Share2 size={14} />
                  <span className='align-middle d-none d-sm-block'>Social</span>
                </NavLink>
              </NavItem>*/}
            </Nav>
            <TabContent activeTab={activeTab}>
              <TabPane tabId='1'>
                <AccountTab selectedUser={store.selectedUser} />
              </TabPane>
            </TabContent>
          </CardBody>
        </Card>
      </Col>
    </Row>
  )
}
export default UserEdit
