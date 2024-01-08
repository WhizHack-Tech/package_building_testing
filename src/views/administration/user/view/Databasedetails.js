// ================================================================================================
//  File Name: Databasedetails.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import React, { useState } from 'react'
import {
  Card,
  CardBody,
  CardHeader,
  Badge,
  UncontrolledTooltip,
  Label,
  Col,
  Input,
  Row,
  Button,
  Form,
  Spinner
} from 'reactstrap'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../../constants/api_message'
import { useParams } from 'react-router-dom'
import { token } from '@utils'
import axios from '@axios'
const MySwal = withReactContent(Swal)
import './Loader.css'

const Database = ({ selectedUser }) => {

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
  
  const { id, activated_plan_id } = useParams()
  const [loading, setLoading] = useState(false)

  const databaseUpdateForm = (event) => {
    setLoading(true)
    event.preventDefault()
    const bodyFormData = new FormData(event.target)
    bodyFormData.append('location_id', id)
    bodyFormData.append('activated_plan_id', activated_plan_id)

    axios({
      method: 'post',
      url: '/update-opensearch-connection-details',
      data: bodyFormData,
      headers: { Authorization: token() }
    })
      .then((res) => {
        if (res.data.message_type === 'success') {
          MySwal.fire({
            title: api_msg.title_msg,
            text: 'Sit Back and Relax',
            icon: 'success',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
          })
        } else if (res.data.message_type === 'unsuccessful') {
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
        setLoading(false)
      })
      .catch((errors) => {
        setLoading(false)
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

  if (!selectedUser || !selectedUser.data) {
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

  return (
    <Card>
      <div style={{ height: '210px' }}>
        <CardHeader className='d-flex justify-content-between align-items-center pt-75 pb-1'>
          <h5 className='mb-0'>Database Details</h5>
          <Badge id='plan-expiry-date' color='light-primary'>
            Tue Jul 04 2023
          </Badge>
          <UncontrolledTooltip placement='top' target='plan-expiry-date'>
            Start Date
          </UncontrolledTooltip>
        </CardHeader>

        <CardBody>
          <Form onSubmit={databaseUpdateForm}>
            <Row>
              <Col sm='6'>
                <Label>Database Username</Label>
                <Input type='text' defaultValue={selectedUser.data.db_username || ''} name='db_username' />
              </Col>
              {/* <input type='hidden' name='id' value={id} /> */}
              <Col sm='6'>
                <Label>Database Password</Label>
                <Input type='text' defaultValue={selectedUser.data.db_password || ''} name='db_password' />
              </Col>
              <Col sm='6'>
                <Label>Database Port</Label>
                <Input type='text' defaultValue={selectedUser.data.db_port || ''} name='db_port' />
              </Col>
              <Col sm='6'>
                <Label>Database Host</Label>
                <Input type='text' defaultValue={selectedUser.data.db_host || ''} name='db_host' />
              </Col>
            </Row>
            <Col className='mt-2 d-flex justify-content-end' sm='12'>
              {loading ? (
                <Spinner color='primary' />
              ) : (
                <Button color='primary' className='btn-submit'>
                  Submit
                </Button>
              )}
            </Col>
          </Form>
        </CardBody>
      </div>
    </Card>
  )
}

export default Database
