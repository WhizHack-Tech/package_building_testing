// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( Eidt User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
// ** User Edit Components
import AccountTab from './Account'
// ** Store & Actions
import { getUser } from '../store/action'
import { useSelector, useDispatch } from 'react-redux'

// ** Third Party Components
import { User } from 'react-feather'
import { Card, CardBody, Row, Col, Nav, NavItem, NavLink, TabContent, TabPane, Spinner } from 'reactstrap'

// ** Styles
import '@styles/react/apps/app-users.scss'

const UserEdit = () => {
  // ** States & Vars
  const [activeTab, setActiveTab] = useState('1'),
    store = useSelector(state => state.users),
    dispatch = useDispatch(),
    { id, activated_plan_id } = useParams()

  // ** Function to toggle tabs
  const toggle = tab => setActiveTab(tab)

  // ** Function to get user on mount
  useEffect(() => {
    dispatch(getUser(id, activated_plan_id))
  }, [dispatch])

  if (store.loader  === true) {
    return <div className='d-flex justify-content-center'><Spinner color='primary' type='grow' /></div>
  } else {
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
  
}
export default UserEdit
