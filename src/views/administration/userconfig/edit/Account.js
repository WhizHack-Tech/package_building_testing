// ================================================================================================
//  File Name:  Account.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
// ** React Imports
import { useState, useEffect } from 'react'
import axios from '@axios'
import { token } from '@utils'
import { useParams } from 'react-router-dom'
// ** Custom Components
import Avatar from '@components/avatar'

// ** Third Party Components
import { Row, Col, Button, Form, Input, Label, FormGroup, Spinner } from 'reactstrap'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../../constants/api_message"
const MySwal = withReactContent(Swal)
const UserAccountTab = ({ selectedUser }) => {
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
      headers: { Authorization: token() }

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
        </Col>
        <Col sm='12'>
          <Form onSubmit={submit_form}>
            <Row>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>secondary Email Id</Label>
                  <Input type='text' name="Lastname" defaultValue={userData.last_name} />
                </FormGroup>
                <input type="hidden" name="id" value={id} />
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label for='name'>Email</Label>
                  <Input type='text' name="organization_secondary_contact_number" defaultValue={userData.email} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label for='email'>Country</Label>
                  <Input type='text' name="organization_city" defaultValue={userData.country} />
                </FormGroup>
              </Col>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>Contact</Label>
                  <Input type='text' name="organization_state" defaultValue={userData.contact_number} />
                </FormGroup>
              </Col>
              <Col className='d-flex flex-sm-row flex-column mt-2' sm='12'>
                {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'> Save Changes</Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' /> &nbsp;Loading... </Button.Ripple>}
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
