// ================================================================================================
//  File Name: Account.js
//  Description: Details of the Administration ( Eidt User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { useState, useEffect } from 'react'
import axios from '@axios'
import { token } from '@utils'
import { useParams } from 'react-router-dom'
// ** Custom Components
import Avatar from '@components/avatar'

// ** Third Party Components
import { Edit } from 'react-feather'
import { Media, Row, Col, Button, Form, Input, Label, FormGroup, Spinner } from 'reactstrap'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../../constants/api_message"
const MySwal = withReactContent(Swal)
const UserAccountTab = ({ selectedUser }) => {
  if (selectedUser === null) {
    return <div className='d-flex justify-content-center'><Spinner color='primary' type='grow' /></div>
  }
  // ** States
  const [img, setImg] = useState(null)
  const [userData, setUserData] = useState(null)
  const [btnLoader, setBtnLoader] = useState(false) 
  const { id } = useParams()
  

  // ** Function to change user image
  const onChange = e => {
    const reader = new FileReader(),
      files = e.target.files
    reader.onload = function () {
      setImg(reader.result)
    }
    reader.readAsDataURL(files[0])
  }

  // ** Update user image on mount or change
  useEffect(() => {
    if (selectedUser !== null || (selectedUser !== null && userData !== null && selectedUser.id !== userData.id)) {
      setUserData(selectedUser)
      if (selectedUser.avatar) {
        return setImg(selectedUser.avatar)
      } else {
        return setImg(null)
      }
    }
  }, [])
function submit_form(event) {
  setBtnLoader(true)
    event.preventDefault()
  
  const bodyFormData = new FormData(event.target)
 
  axios({
    method: "post",
    url: "/users",
    data: bodyFormData,
    headers: { Authorization: token()}
    
  })
    .then((res) => {
      setBtnLoader(false)
      if (res.data.message_type === "successfully_inserted") {
         MySwal.fire({
          title: api_msg.title_msg,
          text: 'Sit Back and Relax',
          icon: 'success',
          customClass: {
            confirmButton: 'btn btn-primary'
          },
          buttonsStyling: false
        })     

      } else if (res.data.message_type === "unsuccessful") {
          MySwal.fire({
            icon: 'error',
            title: api_msg.title_err,
            text: 'Something went wrong!',
            // footer: '<a href="#">Why do I have this issue?</a>',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
           buttonsStyling: false
          }) 
        }
    })
    .catch((errors) => {
      setBtnLoader(false)
       MySwal.fire({
        icon: 'error',
        title: 'Oops!',
        text: 'Something went wrong!',
        // footer: '<a href="#">Why do I have this issue?</a>',
        customClass: {
          confirmButton: 'btn btn-primary'
        },
       buttonsStyling: false
      }) 
    })
}

  // ** Renders User
  const renderUserAvatar = () => {
    if (img === null) {
      const stateNum = Math.floor(Math.random() * 6),
        states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
        color = states[stateNum]
      return (
        <Avatar
          initials
          color={color}
          className='rounded mr-2 my-25'
          content={selectedUser.first_name}
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
    } else {
      return (
        <img
          className='user-avatar rounded mr-2 my-25 cursor-pointer'
          src={img}
          alt='user profile avatar'
          height='90'
          width='90'
        />
      )
    }
  }
  if (userData === null || userData === undefined) {
    return null
  } else {
    return (
      <Row>
        <Col sm='12'>
          <Media className='mb-2'>
            {renderUserAvatar()}
            <Media className='mt-50' body>
              <h4>{selectedUser.first_name} </h4>
              <div className='d-flex flex-wrap mt-1 px-0'>
                <Button.Ripple id='change-img' tag={Label} className='mr-75 mb-0' color='primary'>
                  <span className='d-none d-sm-block'>Change</span>
                  <span className='d-block d-sm-none'>
                    <Edit size={14} />
                  </span>
                  <input type='file' hidden id='change-img' onChange={onChange} accept='image/*' />
                </Button.Ripple>
              </div>
            </Media>
          </Media>
        </Col>
        <Col sm='12'>
        <Form onSubmit={submit_form}>
            <Row>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>FirstName</Label>
                  <Input type='text' name="first_name" defaultValue={userData.first_name} />
                </FormGroup>
                <input type="hidden" name="user_id" value={id} />
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label for='name'>LastName</Label>
                  <Input type='text' name="last_name" defaultValue={userData.last_name} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label for='email'>UserName</Label>
                  <Input type='text' name="username" defaultValue={userData.username} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>contact Number</Label>
                  <Input type='text' name="contact_number" defaultValue={userData.contact_number} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>Gender</Label>
                  <Input type='text' name="username" defaultValue={userData.gender} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>Addrerss-1</Label>
                  <Input type='text' name="username" defaultValue={userData.address_1} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>Address-2</Label>
                  <Input type='text' name="username" defaultValue={userData.address_2} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>State</Label>
                  <Input type='text' name="organization_pincode" defaultValue={userData.state} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>City</Label>
                  <Input type='text' name="organization_pincode" defaultValue={userData.city} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>Zipcode</Label>
                  <Input type='text' name="organization_pincode" defaultValue={userData.zipcode} />
                </FormGroup>
              </Col>
              <Col className='d-flex flex-sm-row flex-column mt-2' sm='12'>
              {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'> Submit </Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' />&nbsp;Loading... </Button.Ripple>}
                <Button.Ripple color='secondary' type='reset' outline>
                  Reset
                </Button.Ripple>
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
    )
  }
}
export default UserAccountTab
