   // ================================================================================================
//  File Name: index.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
// ** React Imports
import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'

// ** Store & Actions
import { getUser } from '../store/action'
import { useSelector, useDispatch } from 'react-redux'

// ** Reactstrap
import { Row, Col, Alert } from 'reactstrap'

// ** User View Components
import UserInfoCard from './UserInfoCard'
import UserTabs from './Tabs'

// ** Styles
import '@styles/react/apps/app-users.scss'

const UserView = props => {
  // ** States
  const [active, setActive] = useState('1')
  const [loading, setLoading] = useState(false)
  // ** Vars
  const store = useSelector(state => state.users),
    dispatch = useDispatch(),
    { id } = useParams()
  // ** Get  data from Store
  useEffect(() => {
    setLoading(true)
    dispatch(getUser(id))
  }, [dispatch])
  // ** Active Tabs 
  const toggleTab = tab => {
    if (active !== tab) {
      setActive(tab)
    }
  }
  return (
    <div className='app-user-view'>
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
export default UserView
