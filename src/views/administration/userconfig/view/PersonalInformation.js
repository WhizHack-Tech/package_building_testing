// ================================================================================================
//  File Name: Personlinformation.js
//  Description: Details of the Administration ( View User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import {  Row, Col, Button, Form, Input, Label, FormGroup, Table, CustomInput, Spinner, CardBody, CardHeader, CardTitle } from 'reactstrap'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from '@axios'
import { token } from '@utils'
import "../Loader.css"
const UserAccountTab = () => {
const {id} = useParams()
const [billData, setBillData] = useState(null)

useEffect(() => {
  axios.get(`/displayuser/${id}/`, { headers: { Authorization: token()} }).then(response => {
    setBillData(response.data)
  })  
}, [])

  // ** Function to change user image
 
    return (
       (billData === null) ?    <div className='d-flex justify-content-center align-items-center' style={{ height: '210px' }}>
       <div class="tri-color-ripple-spinner">
       <div class="ripple ripple1"></div>
       <div class="ripple ripple2"></div>
     </div>
     </div> :  <Row>
         <CardHeader>
          <CardTitle tag='h4'>Address Details</CardTitle>
        </CardHeader>
        <CardBody>
    <Col sm='12'>
        <Form>
            <Row>
              <Col md='6'>
                <FormGroup>
                  <Label>Gender</Label>
                  <Input type='text' value={billData.gender} />
                </FormGroup>
              </Col>
              <Col sm='6'>
                <FormGroup>
                  <Label>Address-1</Label>
                  <Input type='text' value={billData.address_1} />
                </FormGroup>
              </Col>  
              <Col sm='6'>
                <FormGroup>
                  <Label>Address-2</Label>
                  <Input type='text' value={billData.address_2} />
                </FormGroup>
              </Col>  
              <Col sm='6'>
                <FormGroup>
                  <Label>Branch Code</Label>
                  <Input type='text' value={billData.branch_code} />
                </FormGroup>
              </Col> 
              <Col sm='6'>
                <FormGroup>
                  <Label>State</Label>
                  <Input type='text' value={billData.state} />
                </FormGroup>
              </Col>
              <Col sm='6'>
                <FormGroup>
                  <Label>City</Label>
                  <Input type='text' value={billData.city} />
                </FormGroup>
              </Col>  
              <Col sm='6'>
                <FormGroup>
                  <Label>Zipcode</Label>
                  <Input type='text' value={billData.zipcode} />
                </FormGroup>
              </Col>           
            </Row>
          </Form>
        </Col>
        </CardBody>
      </Row>
     
    )
  }

export default UserAccountTab
