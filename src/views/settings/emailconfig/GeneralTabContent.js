import { Component, Fragment, useState } from 'react'
 import axios from '@axios'
 import { token } from '@utils'
 import { Label, FormGroup, Row, Col, Input, Form, Button, Spinner } from 'reactstrap'
 import InputPasswordToggle from '@components/input-password-toggle'
 import Swal from 'sweetalert2'
 import withReactContent from 'sweetalert2-react-content'
 import api_msg from "../../../constants/api_message"
 const MySwal = withReactContent(Swal)
function  AccountDetails() {
const [btnLoader, setBtnLoader] = useState(false) 
const url = "/emailconfigtodb"
const [data, setData] = useState({
    host: '',
    port: '',
    auth: '',
    auth_type: '',
    username: '',
    password: ''
})

function submit(e) {
  setBtnLoader(true)
  e.preventDefault()
  axios.post(url, {
    host: data.host,
    port: data.port,
    auth: data.auth,
    auth_type: data.auth_type,
    username: data.username,
    password: data.password
  }, { headers: { Authorization: token()} })
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
      }).then(function() {
        window.location = "/settings/email"
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

function handle(e) {
  const newdata = {...data}
  newdata[e.target.id] = e.target.value
  setData(newdata)
  console.log(newdata)
}
 
  return (
    <Fragment>
      <Form onSubmit={(e) => submit(e)}>
        <Row>
          <FormGroup tag={Col} md='6'>
            <Label className='form-label'>
              Host
            </Label>
            <Input type='text' value={data.host} id="host" onChange={(e) => handle(e)} required />
          </FormGroup>
          <FormGroup tag={Col} md='6'>
            <Label className='form-label'>
           Port
            </Label>
            <Input type='text' value={data.port} id="port" onChange={(e) => handle(e)} required />
          </FormGroup>
          <FormGroup tag={Col} md='6'>
          <Label>Auth</Label>
          <Input type='select' id='auth' name={data.auth} required onChange={(e) => handle(e)}>
            <option value='0'>--Select--</option>
            <option value='1'>True</option>
            <option value='2'>Flase</option>
          </Input>
        </FormGroup>
        <FormGroup tag={Col} md='6'>
          <Label>Auth-Type</Label>
          <Input type='select' id='auth_type' name={data.auth_type} required onChange={(e) => handle(e)} >
            <option value='0'>--Select--</option>
            <option value='1'>None</option>
            <option value='2'>TLS</option>
            <option value='3'>SSL</option>
          </Input>
        </FormGroup>
        <FormGroup tag={Col} md='6'>
            <Label className='form-label'>
            User Name
            </Label>
            <Input type='text' value={data.username} id="username" onChange={(e) => handle(e)} required />
          </FormGroup>
          <FormGroup tag={Col} md='6'>
            <Label className='form-label'>
              Password
            </Label>
            <InputPasswordToggle
                  required
                  id='password'
                  name={data.password}
                  className='input-group-merge'
                  placeholder='Shared Secret Key'
                  onChange={(e) => handle(e)}
                />
          </FormGroup>
          {/* <FormGroup tag={Col} md='6'>
            <Label className='form-label'>
            Password
            </Label>
            <InputPasswordToggle type='password' value={data.password} id="password" onChange={(e) => handle(e)} />
          </FormGroup> */}
        </Row>
        <Col className='mt-1' sm='12'>
        {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'> Submit </Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' /> Loading... </Button.Ripple>} 
            <Button.Ripple color='secondary' outline type="button">
              Cancel
            </Button.Ripple>
          </Col>
      </Form>
    </Fragment>
  )
}

export default AccountDetails