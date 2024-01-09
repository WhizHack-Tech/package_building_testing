// ================================================================================================
//  File Name: Billingedit.js
//  Description: Details of the Setting ( Billing Edit ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import {  Row, Col, Button, Form, Input, Label, FormGroup, Table, CustomInput, Spinner } from 'reactstrap'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from '@axios'
import { token } from '@utils'
import "../Loader.css"
const UserAccountTab = () => {
const {id} = useParams()
const [billData, setBillData] = useState(null)

useEffect(() => {
  axios.get(`/billinglist/${id}/`, { headers: { Authorization: token()} }).then(response => {
    if (response.data.message_type === 'data_found') {
      setBillData(response.data.data)
    }
  })  
}, [])

const billingUpdateForm = (event) => {
  event.preventDefault()
  const bodyFormData = new FormData(event.target)
 
  axios({
    method: "post",
    url: "/users",
    data: bodyFormData
    
  })
    .then((res) => {
      if (res.data.message_type === "successfully_inserted") {
        //  MySwal.fire({
        //   title: api_msg.title_msg,
        //   text: 'Sit Back and Relax',
        //   icon: 'success',
        //   customClass: {
        //     confirmButton: 'btn btn-primary'
        //   },
        //   buttonsStyling: false
        // })     

      } else if (res.data.message_type === "unsuccessful") {
          // MySwal.fire({
          //   icon: 'error',
          //   title: api_msg.title_err,
          //   text: 'Something went wrong!',
          //   // footer: '<a href="#">Why do I have this issue?</a>',
          //   customClass: {
          //     confirmButton: 'btn btn-primary'
          //   },
          //  buttonsStyling: false
          // }) 
        }
    })
    .catch((errors) => {
      //  MySwal.fire({
      //   icon: 'error',
      //   title: 'Oops!',
      //   text: 'Something went wrong!',
      //   // footer: '<a href="#">Why do I have this issue?</a>',
      //   customClass: {
      //     confirmButton: 'btn btn-primary'
      //   },
      //  buttonsStyling: false
      // }) 
    })
}

  // ** Function to change user image
 
    return (
       (billData === null) ? <div  className='d-flex justify-content-center align-items-center' style={{ height: '300px' }}>
       <div class="tri-color-ripple-spinner">
       <div class="ripple ripple1"></div>
       <div class="ripple ripple2"></div>
       </div>
       </div> :  <Row>
        <Col sm='12'>
        <Form onSubmit={billingUpdateForm}>
            <Row>
              <Col md='4' sm='12'>
                <FormGroup>
                  <Label>Billing name</Label>
                  <Input type='text' name="billing_name"  defaultValue={billData.billing_types} />
                </FormGroup>
                <input type="hidden" name="id" value={id} />
              </Col>
              <Col sm='4'>
                <FormGroup>
                  <Label>Billing Description</Label>
                  <Input type='text' name="billing_decscription" defaultValue={billData.billing_descriptions} />
                </FormGroup>
              </Col>             
              <Col className='d-flex flex-sm-row flex-column mt-2' sm='12'>
                <Button.Ripple className='mb-1 mb-sm-0 mr-0 mr-sm-1' type='submit' color='primary'>
                  Save Changes
                </Button.Ripple>                
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
     
    )
  }

export default UserAccountTab
