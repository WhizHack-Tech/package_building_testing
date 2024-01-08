// ** React Imports
import { useEffect } from 'react'
// import { useParams, Link } from 'react-router-dom'

// ** Reactstrap
import { Row, Col, Alert } from 'reactstrap'

// ** User View Components
import PermissionsTable from './PermissionsTable'

// ** Styles
import '@styles/react/apps/app-users.scss'

const UserView = props => {
  // ** Vars
  // const store = useSelector(state => state.users),
  //   dispatch = useDispatch(),
  //   { id } = useParams()

  // // ** Get suer on mount
  // useEffect(() => {
  //   dispatch(getUser(parseInt(id)))
  // }, [dispatch])

  return (
    <div>
      <Row>
        <Col md='12'>
          <PermissionsTable />
      </Col>
      </Row>
    </div>
  // ) : (
  //   <Alert color='danger'>
  //     <h4 className='alert-heading'>Users not found</h4>
  //     {/* <div className='alert-body'>
  //       Users with id: {id} doesn't exist. Check list of all Users: <Link to='/app/user/list'>Users List</Link>
  //     </div> */}
  //   </Alert>
 )
}
export default UserView
