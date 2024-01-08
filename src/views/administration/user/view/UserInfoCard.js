// ================================================================================================
//  File Name: UserinfoCard.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import { Link } from 'react-router-dom'

// ** Custom Components
import Avatar from '@components/avatar'

// ** Third Party Components
import { Card, CardBody, CardText, CardHeader, Row, Col, Spinner, Badge } from 'reactstrap'
import { Globe, Star, Slack, Smartphone, Cloud, MapPin } from 'react-feather'
import "./Loader.css"
const UserInfoCard = ({ selectedUser }) => {

  if (selectedUser.message_type === null) {
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
  // ** render user img
  const renderUserImg = () => {
    if (selectedUser.message_type === "data_found") {
      const stateNum = Math.floor(Math.random() * 6),
        states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
        color = states[stateNum]
      return (
        <Avatar
          initials
          color={color}
          className='rounded'
          content={selectedUser.data.organization_name}
          contentStyles={{
            borderRadius: 0,
            width: '100%',
            height: '100%'
          }}
          style={{
            height: '50px',
            width: '50px',
            padding: "5px"
          }}
        />
      )
    }
  }

  return (
    <Card style={{ marginBottom: 0 }}>
      <CardHeader className='d-flex justify-content-between align-items-center pt-75 pb-0'>
        <h5 className='mb-0'></h5>
        <Badge id='plan-expiry-date' color='light-primary'>
          {selectedUser.message_type === "data_found" ? new Date(selectedUser.data.created_at).toDateString() : ''}
        </Badge>
      </CardHeader>
      <CardBody>
        <Row>
          <Col xl='12' lg='12' className='d-flex flex-column justify-content-between border-container-lg'>
            <div className='user-avatar-section'>
              <div className='d-flex justify-content-start align-items-center'>
                {renderUserImg()}
                <div className='d-flex flex-column ml-1 mt-2'>
                  <div className='user-info mb-1'>
                    <h4 className='mb-0'>{selectedUser.message_type === "data_found" ? selectedUser.data.organization_name : ''}</h4>
                    <CardText tag='span'>
                      {selectedUser.message_type === "data_found" ? selectedUser.data.email : ''}
                    </CardText>
                  </div>
                  {/* <div className='d-flex flex-wrap align-items-center'>
                    <Button.Ripple tag={Link} to={`/administration/user/edit/${selectedUser.organization_id}`} color='primary'>
                      Edit
                    </Button.Ripple>
                  </div> */}
                </div>
              </div>
            </div>
            <div className='user-info-wrapper'>
              <div className='d-flex flex-wrap align-items-center'>
                <div className='user-info-title'>
                  <Smartphone className='mr-1' size={14} />

                  <CardText tag='span' className='user-info-title font-weight-bold mb-0'>
                    Phone
                  </CardText>
                </div>
                <CardText className='mb-0'>
                  {selectedUser.message_type === "data_found" ? selectedUser.data.phone_number : ''}
                </CardText>
              </div>
              <div className='d-flex flex-wrap align-items-center my-50'>
                <div className='user-info-title'>
                  <Slack className='mr-1' size={14} />
                  <CardText tag='span' className='user-info-title font-weight-bold mb-0'>
                    City
                  </CardText>
                </div>
                <CardText className='text-capitalize mb-0'>
                  {selectedUser.message_type === "data_found" ? selectedUser.data.city : ''}
                </CardText>
              </div>
              <div className='d-flex flex-wrap align-items-center my-50'>
                <div className='user-info-title'>
                  <Star className='mr-1' size={14} />
                  <CardText tag='span' className='user-info-title font-weight-bold mb-0'>
                    State
                  </CardText>
                </div>
                <CardText className='text-capitalize mb-0'>
                  {selectedUser.message_type === "data_found" ? selectedUser.data.state : ''}
                </CardText>
              </div>
              <div className='d-flex flex-wrap align-items-center my-50'>
                <div className='user-info-title'>
                  <Cloud className='mr-1' size={14} />
                  <CardText tag='span' className='user-info-title font-weight-bold mb-0'>
                    Country
                  </CardText>
                </div>
                <CardText className='mb-0'>{selectedUser.message_type === "data_found" ? selectedUser.data.country_name : ''}</CardText>
              </div>
              <div className='d-flex flex-wrap align-items-center'>
                <div className='user-info-title'>
                  <MapPin className='mr-1' size={14} />
                  <CardText tag='span' className='user-info-title font-weight-bold mb-0'>
                    Pincode
                  </CardText>
                </div>
                <CardText className='mb-0'>{selectedUser.message_type === "data_found" ? selectedUser.data.pincode : ''}</CardText>
              </div>
            </div>
          </Col>
        </Row>
      </CardBody>
    </Card>
  )
}

export default UserInfoCard
