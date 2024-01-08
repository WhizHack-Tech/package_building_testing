// ================================================================================================
//  File Name: Planedit.js
//  Description: Details of the Setting ( Edit Plan ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import { Row, Col, Button, Form, Input, Label, FormGroup, Table, CustomInput, Spinner } from 'reactstrap'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from '@axios'
import { token } from '@utils'
import '../Loader.css'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../constants/api_message'
const MySwal = withReactContent(Swal)

const UserAccountTab = () => {
  const { id } = useParams()
  const [billData, setBillData] = useState(null)
  const [loading, setLoading] = useState(false) // Define loading state

  useEffect(() => {
    axios.get(`/display-updated-plan/${id}/`, { headers: { Authorization: token() } }).then(response => {
      if (response.data.message_type === 'success') {
        setBillData(response.data.data)
      }
    })
  }, [])

  const billingUpdateForm = (event) => {
    event.preventDefault()
    setLoading(true) // Set loading state to true

    const bodyFormData = new FormData(event.target)

    axios({
      method: 'post',
      url: `/plan2-update-details`,
      data: bodyFormData,
      headers: { Authorization: token() }
    })
    .then((res) => {
      if (res.data.message_type === 'updated_successfully') {
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
      setLoading(false) // Set loading state to false
    })
    .catch((errors) => {
      setLoading(false) // Set loading state to false
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
    (billData === null) ? <div className='d-flex justify-content-center align-items-center' style={{ height: '300px' }}>
      <div class="tri-color-ripple-spinner">
        <div class="ripple ripple1"></div>
        <div class="ripple ripple2"></div>
      </div>
    </div> : <Row>
      <Col sm='12'>
        <Form onSubmit={billingUpdateForm}>
          <Row>
            <Col md='4' sm='12'>
              <FormGroup>
                <Label>Plan name</Label>
                <Input type='text' name="plan_name" defaultValue={billData.plan_name} />
              </FormGroup>
              <input type="hidden" name="plan_id" value={id} />
            </Col>
            <Col sm='4'>
              <FormGroup>
                <Label>Plan Description</Label>
                <Input type='text' name="plan_descriptions" defaultValue={billData.plan_descriptions} />
              </FormGroup>
            </Col>
            <Col sm='4'>
              <FormGroup>
                <Label>Plan Start Date</Label>
                <Input type='text' name="plan_start-date" defaultValue={billData.plan_start_date} disabled />
              </FormGroup>
            </Col>
            <Col sm='4'>
              <FormGroup>
                <Label>Plan End Date</Label>
                <Input type='text' name="plan_end_date" defaultValue={billData.plan_end_date} disabled />
              </FormGroup>
            </Col>
            <Col sm='4'>
              <FormGroup>
                <Label>Plan Created Date</Label>
                <Input type='text' name="Created Date" defaultValue={billData.plan_creations_timestamp} disabled />
              </FormGroup>
            </Col>
            <Col className='mt-2 d-flex justify-content-end' sm='12'>
              {loading ? (
                <Spinner color='primary' />
              ) : (
                <Button color='primary' className='btn-submit'>
                  Save Changes
                </Button>
              )}
            </Col>
          </Row>
        </Form>
      </Col>
    </Row>
  )
}

export default UserAccountTab
