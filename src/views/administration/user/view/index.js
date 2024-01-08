// ================================================================================================
//  File Name: index.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** React Imports
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import BreadCrumbs from '@components/breadcrumbs'

// ** Store & Actions
import { getUser } from '../store/action'
import { useSelector, useDispatch } from 'react-redux'

// ** Reactstrap
import { Row, Col, Card, CardBody } from 'reactstrap'

// ** User View Components
import PlanCard from './PlanCard'
import UserInfoCard from './UserInfoCard'
import BasicTimeline from './BasicTimeline'
import TableZeroConfig from './TableZeroConfig'
import Database from './Databasedetails'
// ** Styles
import '@styles/react/apps/app-users.scss'

const UserView = props => {
  // ** Vars
  const store = useSelector(state => state.users),
    dispatch = useDispatch(),
    { id, activated_plan_id } = useParams()

  // ** Get suer on mount
  useEffect(() => {

    dispatch(getUser(id, activated_plan_id))
  }, [])

  return <div className='app-user-view'>
    <BreadCrumbs breadCrumbTitle='Organization Details' />
    <Row className='match-height'>
      <Col xl='4' lg='5' md='5'>
        <Card className='plan-card border-primary'>
          <UserInfoCard selectedUser={store.selectedUser} />
        </Card>
      </Col>
      <Col xl='4' lg='5' md='5'>
        <Card className='plan-card border-primary'>
          <PlanCard selectedUser={store.selectedUser} />
        </Card>
      </Col>
      <Col xl='4' lg='4' md='5'>
        <Card className='plan-card border-primary'>
          <Database selectedUser={store.selectedUser} />
        </Card>
      </Col>
    </Row>
    <Row>
      <Col xl='12' lg='12' md='12' sm='12'>
        <Card className='plan-card border-primary'>
          <CardBody>
            <BasicTimeline />
          </CardBody>
        </Card>
      </Col>

    </Row>
  </div>
}
export default UserView