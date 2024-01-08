// ================================================================================================
//  File Name: UserInfoCard.js
//  Description: Details of the Administration ( View User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { Link } from 'react-router-dom'
import Avatar from '@components/avatar'
import "../Loader.css"
// ** Third Party Components
import { Card, CardBody, Button, Badge, Spinner } from 'reactstrap'
const roleColors = {
  editor: 'light-info',
  admin: 'light-danger',
  author: 'light-warning',
  maintainer: 'light-success',
  subscriber: 'light-primary'
}

const UserInfoCard = ({ selectedUser }) => {

  if (selectedUser === null) {
    return (
      <Card>
        <CardBody className='d-flex justify-content-center align-items-center' style={{ height: '210px' }}>
        <div class="tri-color-ripple-spinner">
            <div class="ripple ripple1"></div>
            <div class="ripple ripple2"></div>
          </div>
        </CardBody>
      </Card>
    )
  }
  const renderUserImg = () => {
    if (selectedUser !== null && selectedUser.avatar) {
      return <img src={selectedUser.avatar} alt='user-avatar' className='img-fluid rounded' height='104' width='104' />
    } else {
      const stateNum = Math.floor(Math.random() * 6),
        states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
        color = states[stateNum]
      return (
        <Avatar
          initials
          color={color}
          className='rounded'
          content={selectedUser !== null ? selectedUser.first_name : 'Eleanor Aguilar'}
          contentStyles={{
            borderRadius: 0,
            fontSize: 'calc(36px)',
            width: '100%',
            height: '100%'
          }}
          style={{
            height: '90px',
            width: '90px'
          }}
        />
      )
    }
  }

  return (
    <Card>
        <CardBody>
          <div className='user-avatar-section'>
            <div className='d-flex align-items-center flex-column'>
              {renderUserImg()}
              <div className='d-flex flex-column align-items-center text-center'>
                <div className='user-info mt-1' >
                  <h4>{selectedUser !== null ? selectedUser.first_name  : 'Eleanor Aguilar'} {selectedUser !== null ? selectedUser.last_name  : 'Eleanor Aguilar'}</h4>
                  {selectedUser !== null ? (
                    <Badge color={roleColors[selectedUser.first_name]} className='text-capitalize'>
                    </Badge>
                  ) : null}
                </div>
              </div>
            </div>
          </div>
          <h4 className='fw-bolder border-bottom pb-50 mb-1'>Details</h4>
          <div className='info-container'>
            {selectedUser !== null ? (
              <ul className='list-unstyled'>
                 <li className='mb-75'>
                  <span className='fw-bolder me-25'>Account Status :</span>
                  <span className='ml-1'><Badge color='light-info'>{selectedUser.is_active ? 'Active' : 'Deactive'}</Badge></span>
                </li>
                {/* <li className='mb-75'>
                  <span className='fw-bolder me-25'>Username :</span>
                  <span className='ml-1'>{selectedUser.username}</span>
                </li> */}
                <li className='mb-75'>
                  <span className='fw-bolder me-25'>Email :</span>
                  <span className='ml-1'>{selectedUser.email}</span>
                </li>
                <li className='mb-75'>
                  <span>Organization name :</span>
                  <span className='ml-1'>{selectedUser.organization_name}</span>
                </li>
                <li className='mb-75'>
                  <span className='fw-bolder me-25'>Contact :</span>
                  <span className='ml-1'>{selectedUser.contact_number}</span>
                </li>
              </ul>
            ) : null}
          </div>
          <h4 className='fw-bolder border-bottom pb-50 mb-1'>Location Details</h4>
          <div className='info-container'>
            {selectedUser !== null ? (
              <ul className='list-unstyled'>
                 <li className='mb-75'>
                  <span className='fw-bolder me-25'>Branch Code:</span>
                  <span className='ml-1'><Badge color='light-primary'>{selectedUser.location_branchcode}</Badge></span>
                </li>
                <li className='mb-75'>
                  <span className='fw-bolder me-25'>City :</span>
                  <span className='ml-1'>{selectedUser.location_city}</span>
                </li>
                <li className='mb-75'>
                  <span>State/Region:</span>
                  <span className='ml-1'>{selectedUser.location_state}</span>
                </li>
                <li className='mb-75'>
                  <span className='fw-bolder me-25'>Country :</span>
                  <span className='ml-1'>{selectedUser.country_name}</span>
                </li>
                <li className='mb-75'>
                  <span className='fw-bolder me-25'>Pincode :</span>
                  <span className='ml-1'>{selectedUser.location_pincode}</span>
                </li>
              </ul>
            ) : null}
          </div>
          {/* <div className='d-flex justify-content-center pt-2'>
          <Button.Ripple tag={Link} to={`/administration/userconfig/edit/${selectedUser !== null ? selectedUser.id : 'Eleanor Aguilar'}`} color='primary'>
                      Edit
                    </Button.Ripple>
          </div> */}
        </CardBody>
      </Card>
  )
}

export default UserInfoCard
