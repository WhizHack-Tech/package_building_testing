// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( View User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import BreadCrumbs from '@components/breadcrumbs'

// ** Store & Actions
import { singleClient } from '../store/action'
import { useSelector, useDispatch } from 'react-redux'

// ** Reactstrap
import { Row, Col, Alert, Spinner } from 'reactstrap'
import "../Loader.css"
// ** User View Components
import UserInfoCard from './UserInfoCard'
import UserTabs from './Tabs'

// ** Styles
import '@styles/react/apps/app-users.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'

const UserView = props => {
 
  const store = useSelector(state => state.client_users),
    dispatch = useDispatch(),
    { id } = useParams()
    
  useEffect(() => {
    dispatch(singleClient(id))
  }, [dispatch])

  const [active, setActive] = useState('1')

  const toggleTab = tab => {
    if (active !== tab) {
      setActive(tab)
    }
  }

  if (store.loader  === true) {
    return <div className='d-flex justify-content-center'> <div class="tri-color-ripple-spinner">
    <div class="ripple ripple1"></div>
    <div class="ripple ripple2"></div>
  </div></div>
  } else {
    return (
      <div className='app-user-view'>
        <BreadCrumbs breadCrumbTitle='User Config Details'/>
        <Row>
          <Col xl='4' lg='5' xs={{ order: 1 }} md={{ order: 0, size: 5 }}>
            <UserInfoCard selectedUser={store.selectedUser} />
          </Col>
          <Col xl='8' lg='7' xs={{ order: 0 }} md={{ order: 1, size: 7 }}>
            <UserTabs active={active} toggleTab={toggleTab} selectedUser={store.selectedUser} />
          </Col>
        </Row>
      </div>
      )
  }

}
export default UserView
