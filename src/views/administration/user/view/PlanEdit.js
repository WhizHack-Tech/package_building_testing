// ================================================================================================
//  File Name: PlanEdit.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================

import React, { useEffect, useState } from 'react'
import { useParams, useHistory } from 'react-router-dom'
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import {
  Card,
  Label,
  Col,
  Input,
  Row,
  Button,
  Spinner,
  Form,
  FormGroup
} from 'reactstrap'
import './Loader.css'
import { useForm, Controller } from 'react-hook-form'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../../constants/api_message'
import Select from 'react-select'

const MySwal = withReactContent(Swal)

const License = () => {
  const history = useHistory()
  const { id } = useParams()
  const [loading, setLoading] = useState(false)
  const [plantype, setPlantype] = useState([])
  const [planData, setPlanData] = useState({
    plan_name: '',
    plan_descriptions: '',
    plan_start_date: '',
    plan_end_date: '',
    plan_creations_timestamp: ''
  })

  const [apiLoading, setApiLoading] = useState(false)

  const { control, handleSubmit, watch } = useForm() // Removed unused variables

  useEffect(() => {
    axios
      .get(`/get-inactive-plans/`, { headers: { Authorization: token() } })
      .then((res) => {
        if (res.data.message_type === 'success') {
          const plantypeList = res.data.data.map((element) => ({
            value: element.id,
            label: `${element.plan_name}`
          }))
          setPlantype(plantypeList)
        }
      })
  }, [])

  // Watch for changes in the selected plan
  const selectedPlan = watch('plan_id')

  useEffect(() => {
    if (selectedPlan) {
      // Fetch plan details when a plan is selected
      setApiLoading(true)
      axios
        .get(`/get-inactive-plans/${selectedPlan}/`, {
          headers: { Authorization: token() }
        })
        .then((res) => {
          if (res.data.message_type === 'success') {
            const planDetails = res.data.data
            setPlanData({
              plan_name: planDetails.plan_name,
              plan_descriptions: planDetails.plan_descriptions,
              plan_start_date: planDetails.plan_start_date,
              plan_end_date: planDetails.plan_end_date,
              plan_creations_timestamp: planDetails.plan_creations_timestamp
            })
          }
          setApiLoading(false)
        })
        .catch((error) => {
          setApiLoading(false)
          console.error('Error fetching plan details:', error)
        })
    } else {
      setPlanData({
        plan_name: '',
        plan_descriptions: '',
        plan_start_date: '',
        plan_end_date: '',
        plan_creations_timestamp: ''
      })
    }
  }, [selectedPlan])

  const lisenceUpdateForm = (data) => {
    setLoading(true)
    axios({
      method: 'post',
      url: `/upgrade-plan?location_id=${id}`,
      data,
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
          }).then((result) => {
            if (result.isConfirmed) {
              history.push('/administration/user/list') // Redirect to another page after success
            }
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

  return (
    <Card>
      {apiLoading ? (
        <div className='d-flex justify-content-center'>
          <div class='tri-color-ripple-spinner'>
            <div class='ripple ripple1'></div>
            <div class='ripple ripple2'></div>
          </div>
        </div>
      ) : (
        <Form onSubmit={handleSubmit(lisenceUpdateForm)}>
          <Row>
            <Col md='4' className='mb-1'>
              <Label for='plan_id'>Plan Type</Label>
              <Controller
                id='plan_id'
                name='plan_id'
                control={control}
                render={({ field: { onChange, value } }) => (
                  <Select
                    name='plan_id'
                    isClearable={true}
                    className='react-select'
                    classNamePrefix='select'
                    options={plantype}
                    theme={selectThemeColors}
                    value={plantype.find((c) => c.value === value) || null}
                    onChange={(val) => {
                      onChange(val?.value || null)
                    }}
                  />
                )}
              />
            </Col>
            <Col sm='4'>
              <FormGroup>
                <Label>Plan Description</Label>
                <Input
                  type='text'
                  name='plan_descriptions'
                  value={planData.plan_descriptions}
                  onChange={(e) => setPlanData({
                      ...planData,
                      plan_descriptions: e.target.value
                    })
                  }
                />
              </FormGroup>
            </Col>
            <Col sm='4'>
              <FormGroup>
                <Label>Plan Start Date</Label>
                <Input
                  type='text'
                  name='Start Date'
                  value={planData.plan_start_date}
                  disabled
                />
              </FormGroup>
            </Col>
            <Col sm='4'>
              <FormGroup>
                <Label>Plan End Date</Label>
                <Input
                  type='text'
                  name='End Date'
                  value={planData.plan_end_date}
                  disabled
                />
              </FormGroup>
            </Col>
            <Col sm='4'>
              <FormGroup>
                <Label>Plan Created Date</Label>
                <Input
                  type='text'
                  name='Created Date'
                  value={planData.plan_creations_timestamp}
                  disabled
                />
              </FormGroup>
            </Col>
          </Row>
          <Col className='mt-2 d-flex justify-content-end' sm='12'>
            {loading ? (
              <Spinner color='primary' />
            ) : (
              <Button color='primary' className='btn-submit' type='submit'>
                Submit
              </Button>
            )}
          </Col>
        </Form>
      )}
    </Card>
  )
}

export default License
