// ================================================================================================
//  File Name: Environment.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect } from 'react'
import { CustomInput, Button, Card, ModalBody, ModalFooter, Label, FormGroup, Input, Col, Row, Spinner, Form } from 'reactstrap'
import axios from '@axios'
import { token } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../constants/api_message"
const MySwal = withReactContent(Swal)
const Environment = () => {
const [btnLoader, setBtnLoader] = useState(false)

  const url_link = "/init-config"
  function submit_form(event) {
    setBtnLoader(true)
    event.preventDefault()

    const bodyFormData = new FormData(event.target)

    axios({
      method: "post",
      url: url_link,
      data: bodyFormData,
      headers: { Authorization: token() }

    })
      .then((res) => {
        setBtnLoader(false)
        if (res.data.message_type === "success") {
          MySwal.fire({
            title: api_msg.title_msg,
            text: 'Sit Back and Relax',
            icon: 'success',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
          })

        } else if (res.data.message_type === "form_errror") {
          MySwal.fire({
            icon: 'error',
            title: api_msg.title_err,
            text: 'Something went wrong!',
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
          customClass: {
            confirmButton: 'btn btn-primary'
          },
          buttonsStyling: false
        })
      })
  }
  
  return (
    <Card>
   <Form onSubmit={submit_form}>
     <Row>
       <Col sm='6'>
         <FormGroup>
           <Label>Email2</Label>
           <Input type='text' name="email_ids"/>
         </FormGroup>
       </Col>
       <Col sm='6'>
       <FormGroup>
              <Label>Severity</Label>
              <Input type='select' name='time_interval_name' required>
                <option value='' disabled selected>---Select---</option>
                <option value='1'>Severity-1</option>
                <option value='2'>Severity-2</option>
                <option value='3'>Severity-3</option>
              </Input>
            </FormGroup>
       </Col>
       <Col sm='6'>
       <FormGroup>
              <Label for='user-role'>Time Interval</Label>
              <Input type='select' name='time_interval_val' required>
                <option value='' disabled selected>---Select---</option>
                <option value='1'>Last 5minutes</option>
                <option value='2'>Last 15minutes</option>
                <option value='3'>Last 30minutes</option>
                <option value='4'>Last 1hour</option>
                <option value='5'>Last 6hours</option>
                <option value='6'>Last 12hours</option>
                <option value='7'>Last 24hours</option>
              </Input>
            </FormGroup>
       </Col>
       <Col className='mt-1' sm='12'>
       {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'> Submit </Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' />&nbsp;Saving... </Button.Ripple>}       </Col>
     </Row>            
   </Form>
</Card>
  )
}

export default Environment
