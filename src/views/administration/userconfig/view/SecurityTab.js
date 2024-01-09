// ================================================================================================
//  File Name: SecurityTab.js
//  Description: Details of the Administration ( View User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { Fragment, useState } from 'react'
import axios from 'axios'

// ** Reactstrap Imports
import {
  Row,
  Col,
  Card,
  Form,
  CardBody,
  Button,
  CardTitle,
  CardHeader,
  Label
} from 'reactstrap'

// ** Custom Components
import InputPassword from '@components/input-password-toggle'

// ** Third Party Components
import 'cleave.js/dist/addons/cleave-phone.us'


const SecurityTab = () => {
  const [oldPassNotMatch, setOldPassNotMatch] = useState(null)
  const [confirmPass, setconfirmPass] = useState(null)

  const resetPasswordForm = (e) => {
    e.preventDefault()
    const formData = new FormData(e.target)
    
         
      if (e.target.new_password.value === e.target.confirm_password.value) {          
        setconfirmPass(null)
        axios({
          url:"https://google.com/s?sai",
          method:"post",
          data:formData
        }).then((res) => {
          console.log(res)
          // setOldPassNotMatch()
        }).catch((error) => {
          console.log(error.message)
        })
      } else {
        setconfirmPass("Your Comfirm password not match")
      }     
}
  return (
    <Fragment>
      <Card>
        <CardHeader>
          <CardTitle tag='h4'>Change Password</CardTitle>
        </CardHeader>
        <CardBody>
          <Form onSubmit={resetPasswordForm}>
            <Row>
          <Col className='mb-2' md={6}>
          <Label className='form-label' for='old-password' autoFocus>
                  Old Password
                </Label>
                <InputPassword className='input-group-merge' id='old-password' name="old_password"  required  />
                {oldPassNotMatch !== null ? <p className='text-danger m-1 p-0'>{oldPassNotMatch}</p> : ''}
            
              </Col>
              </Row>
            <Row>
              <Col className='mb-2' md={6}>
              <Label className='form-label' for='new-password'>
                  New Password
                </Label>
                <InputPassword className='input-group-merge' id='new-password' name="new_password"  required  />
              </Col>
              <Col className='mb-2' md={6}>
              <Label className='form-label' for='confirm-password'>
                  Confirm Password
                </Label>
                <InputPassword className='input-group-merge' id='confirm-password' name="confirm_password" required />
                {confirmPass !== null ? <p className='text-danger m-1 p-0'>{confirmPass}</p> : ''}
              </Col>
              <Col xs={12}>
                <Button type='submit' color='primary'>
                  Change Password
                </Button>
              </Col>
            </Row>
          </Form>
        </CardBody>
      </Card>
    </Fragment>
  )
}

export default SecurityTab
