
import { Component, Fragment, useState } from 'react'
 import axios from '@axios'
 import { Label, FormGroup, Row, Col, Input, Form, Button, NavLink } from 'reactstrap'
 import InputPasswordToggle from '@components/input-password-toggle'

function  AccountDetails() {
const url = "/create/"
const [data, setData] = useState({
    host_name: '',
    port_name: '',
    user_role: '',
    auth_type: '',
    user_name: '',
    password: ''
})

function submit(e) {
  e.preventDefault()
  axios.post(url, {
    host_name: data.host_name,
    port_name: data.port_name,
    user_role: data.user_role,
    auth_type: data.auth_type,
    user_name: data.user_name,
    password: data.password
  })
  .then(res => {
    console.log(res.data)
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
            <Input type='text' value={data.host_name} id="host_name" onChange={(e) => handle(e)} />
          </FormGroup>
          <FormGroup tag={Col} md='6'>
            <Label className='form-label'>
           Port
            </Label>
            <Input type='text' value={data.port_name} id="port_name" onChange={(e) => handle(e)} />
          </FormGroup>
          <FormGroup tag={Col} md='6'>
          <Label>Auth</Label>
          <Input type='select' id='user_role' name={data.user_role} required onChange={(e) => handle(e)}>
            <option value='0'>--Select--</option>
            <option value='1'>Ture</option>
            <option value='2'>Flase</option>
          </Input>
        </FormGroup>
        <FormGroup tag={Col} md='6'>
          <Label>Auth-Type</Label>
          <Input type='select' id='auth_type' name={data.auth_type} required onChange={(e) => handle(e)}>
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
            <Input type='text' value={data.user_name} id="user_name" onChange={(e) => handle(e)} />
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
            <Button.Ripple className='mr-1' color='primary' type='submit'>
              Save changes
            </Button.Ripple>
            <Button.Ripple color='secondary' outline>
              Cancel
            </Button.Ripple>
          </Col>
      </Form>
    </Fragment>
  )
}

export default AccountDetails
