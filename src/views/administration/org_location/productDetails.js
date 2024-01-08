// ================================================================================================
//  File Name: productDetails.js
//  Description: Details of the Administration ( Add Organization Location Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// Import the necessary libraries
import React, { useState, useEffect, Fragment } from 'react'
import { useHistory } from 'react-router-dom'
import { Form, Label, Input, CustomInput, Col, Button, FormGroup, Row, Card } from 'reactstrap'
import styled from 'styled-components'
import axios from '@axios'
import Swal from 'sweetalert2'
import api_msg from "../../../constants/api_message"
import { isObjEmpty, selectThemeColors, token } from '@utils'
import { useForm, Controller } from 'react-hook-form'
import Select from 'react-select'
import { ArrowLeft, ArrowRight } from 'react-feather'
import "flatpickr/dist/flatpickr.css"
import "flatpickr/dist/themes/dark.css"
import Flatpickr from 'react-flatpickr'

// Set default values for validation
const StyledComponent = styled.div`
  margin-bottom: 2px;
`
let locationId = ''

const serchState = () => {
  const searchParams = new URLSearchParams(window.location.search)
  const location_id = searchParams.get('location_id')
  locationId = location_id
  console.log({ locationId })
}

function formatDate(inputDateString) {
  const date = new Date(inputDateString)
  const day = date.getDate().toString().padStart(2, '0') // Get day and pad with leading zero if needed
  const month = (date.getMonth() + 1).toString().padStart(2, '0') // Get month (add 1 as it's zero-based) and pad with leading zero if needed
  const year = date.getFullYear()
  return `${year}-${month}-${day}`
}

const ProductDetails = ({ stepper }) => {
  const [isLoading, setIsLoading] = useState(false)
  const [default_page, setDefault_page] = useState('')
  const [env_trace, setEnv_trace] = useState(false)
  // const [env_wazuh, setEnv_wazuh] = useState(false)
  const [env_nids, setEnv_nids] = useState(false)
  const [env_hids, setEnv_hids] = useState(false)
  const [live_map, setLive_map] = useState(false)

  const [envSoar, setEnvSoar] = useState(false)
  const [healthCheck, setHealthCheck] = useState(false)
  const [mediaManagement, setMediaManagement] = useState(false)
  const [tpThreadFeed, setTpThreadFeed] = useState(false)
  const [sandBox, setSandBox] = useState(false)
  const [ess, setEss] = useState(false)
  const [tpSource, setTpSource] = useState(false)
  const [planData, setPlanData] = useState([])
  const [billData, setBillData] = useState([])
  const { control } = useForm()
  const [plan_id, setPlanId] = useState(null) // Declare plan_id
  const [billing_id, setBillingId] = useState(null)
  const [picker, setPicker] = useState(new Date())
  const [startDate, setStartDate] = useState(new Date())
  const [endDate, setEndDate] = useState(new Date())
  const [description, setDescription] = useState('')
  const [plantype, setPlantype] = useState('')

  const handleStartDateChange = (selectedDates) => {
    // selectedDates is an array, but since we're dealing with a single date, we can use [0]
    setStartDate(selectedDates[0])
  }

  const history = useHistory()

  useEffect(() => {
    axios.get(`/planlist/`, { headers: { Authorization: token() } }).then(res => {
      if (res.data.message_type === "data_found") {
        const planList = []
        if (res.data.data.length > 0) {
          res.data.data.forEach((element, index) => {
            planList[index] = { value: element.id, label: element.plan_name }
          })
        }
        setPlanData(planList)
      }
    })

    axios.get(`/billinglist/`, { headers: { Authorization: token() } }).then(res => {
      if (res.data.message_type === "data_found") {
        const billList = []
        if (res.data.data.length > 0) {
          res.data.data.forEach((element, index) => {
            billList[index] = { value: element.id, label: element.billing_types }
          })
        }
        setBillData(billList)
      }
    })
  }, [])
  const handleSubmit = (event) => {
    setIsLoading(true)
    serchState()
    event.preventDefault()

    const searchParams = new URLSearchParams(window.location.search)
    // Prepare the data to be sent
    const bodyFormData = new FormData()
    bodyFormData.append('default_page', default_page)
    bodyFormData.append('env_nids', env_nids)
    bodyFormData.append('env_hids', env_hids)
    // bodyFormData.append('env_wazuh', env_wazuh)
    bodyFormData.append('env_trace', env_trace)
    bodyFormData.append('location_id', locationId)
    bodyFormData.append('xdr_live_map', live_map)

    bodyFormData.append('env_soar', envSoar)
    bodyFormData.append('env_hc', healthCheck)
    bodyFormData.append('env_mm', mediaManagement)
    bodyFormData.append('env_tptf', tpThreadFeed)
    bodyFormData.append('env_sbs', sandBox)
    bodyFormData.append('env_ess', ess)
    bodyFormData.append('env_tps', tpSource)
    bodyFormData.append('plan_name', plantype) // Add the selected plan ID here
    bodyFormData.append('plan_start_date', formatDate(startDate))
    bodyFormData.append('plan_end_date', formatDate(endDate))
    bodyFormData.append('plan_descriptions', description)


    // Make the POST request using Axios
    axios
      .post('/add-location-step-two', bodyFormData, { headers: { Authorization: token() } })
      .then((response) => {
        setIsLoading(false)

        if (response.data.message_type === "successfully_inserted") {

          searchParams.set('plan_id', response.data.plan_id)
          searchParams.set('location_id', locationId)
          const newUrl = `?${searchParams.toString()}`
          window.history.pushState(null, '', newUrl)
          stepper.next()


        } else if (response.data.message_type === "unsuccessful") {
          Swal.fire({
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
      .catch((error) => {
        setIsLoading(false)
        console.error(error)
        Swal.fire({
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
    <Fragment>
      <Form onSubmit={handleSubmit}>
        <div className='content-header col-12 mt-2'>
          <h5 className='mb-0'>Plan Details</h5>
          <small className='text-muted'>Add  Your Paln Details.</small>
          <hr />
        </div>

        <Row>
          <Col sm='6'>
            <Label>Plan Type</Label>
            <Input
              type='text'
              name='plan_name'
              value={plantype}
              onChange={(e) => setPlantype(e.target.value)} // Update the description state
            />
          </Col>
          <Col sm='6'>
            <Label for="start_date_label">Start Date</Label>
            <Flatpickr
              className='form-control'
              value={startDate}
              id='start_date_label'
              onChange={date => setStartDate(date)}
              name='plan_start_date'
            />

          </Col>
          <Col sm='6'>
            <Label>End Date</Label>
            <Flatpickr
              className='form-control'
              name="plan_end_date"
              value={endDate}
              onChange={(date) => setEndDate(date)}
            />
          </Col>
          <Col sm='6'>
            <Label>Plan Description</Label>
            <Input
              type='textarea'
              name='plan_descriptions'
              value={description}
              onChange={(e) => setDescription(e.target.value)} // Update the description state
            />
          </Col>
        </Row>
        <div className='content-header col-12 mt-2'>
          <h5 className='mb-0'>Page Details</h5>
          <small className='text-muted'>Add  Your Page Details.</small>
          <hr />
        </div>
        <FormGroup>
          <Col sm='2'>
            <Label>Default Page</Label>
            <Input
              type='select'
              value={default_page}
              onChange={(e) => setDefault_page(e.target.value)}
              required
            >
              <option value='' disabled selected>
                ...Select...
              </option>
              <option value='/nids/alerts'>NIDS</option>
              <option value='/hids/alerts'>HIDS</option>
              <option value='/trace/alerts'>Trace</option>
              <option value='/health-check/sensor-health'>Health Check</option>
              <option value='/soar'>Soar</option>
              <option value='/media-management'>Media Management</option>
              <option value='/tp-thread-feed'>TP Thread Feed</option>
              <option value='/sand-box'>Sand Box</option>
              <option value='/ess'>ESS</option>
              <option value='/tp-source'>TP Source</option>
            </Input>
          </Col>
        </FormGroup>

        <div className='mt-3 ml-1'>
          <CustomInput
            type='switch'
            id='exampleCustomSwitch'
            name='customSwitch'
            label='Trace'
            inline
            checked={env_trace}
            onChange={(e) => setEnv_trace(e.target.checked)}
          />

          <CustomInput
            type='switch'
            id='nids'
            name='customSwitch'
            label='NIDS'
            inline
            checked={env_nids}
            onChange={(e) => setEnv_nids(e.target.checked)}
          />

          <CustomInput
            type='switch'
            id='hids'
            name='customSwitch'
            label='HIDS'
            inline
            checked={env_hids}
            onChange={(e) => setEnv_hids(e.target.checked)}
          />

          <CustomInput
            type='switch'
            id='env_soar'
            name='env_soar'
            label='Soar'
            inline
            checked={envSoar}
            onChange={(e) => setEnvSoar(e.target.checked)}
          />

          <CustomInput
            type='switch'
            id='xdr_live_map'
            name='xdr_live_map'
            label='Live Map'
            inline
            checked={live_map}
            onChange={(e) => setLive_map(e.target.checked)}
          />

          <CustomInput
            type='switch'
            id='env_hc'
            name='env_hc'
            label='Health Check'
            inline
            checked={healthCheck}
            onChange={(e) => setHealthCheck(e.target.checked)}
          />
        </div>

        <div className='mt-3 ml-1'>
          <CustomInput
            type='switch'
            id='env_mm'
            name='env_mm'
            label='Media Management'
            inline
            checked={mediaManagement}
            onChange={(e) => setMediaManagement(e.target.checked)}
          />

          {/* <CustomInput
              type='switch'
              id='wazuh'
              name='customSwitch'
              label='Wazuh'
              inline
              checked={env_wazuh}
              onChange={(e) => setEnv_wazuh(e.target.checked)}
            /> */}

          <CustomInput
            type='switch'
            id='env_tptf'
            name='env_tptf'
            label='TP Thread Feed'
            inline
            checked={tpThreadFeed}
            onChange={(e) => setTpThreadFeed(e.target.checked)}
          />

          <CustomInput
            type='switch'
            id='env_sbs'
            name='env_sbs'
            label='Sand Box'
            inline
            checked={sandBox}
            onChange={(e) => setSandBox(e.target.checked)}
          />

          <CustomInput
            type='switch'
            id='env_ess'
            name='env_ess'
            label='ESS'
            inline
            checked={ess}
            onChange={(e) => setEss(e.target.checked)}
          />

          <CustomInput
            type='switch'
            id='env_tps'
            name='env_tps'
            label='TP Source'
            inline
            checked={tpSource}
            onChange={(e) => setTpSource(e.target.checked)}
          />
        </div>

        <div className='d-flex justify-content-between mt-2'>
          <Button type='button' color='primary' className='btn-prev' onClick={() => stepper.previous()}>
            <ArrowLeft size={14} className='align-middle me-sm-25 me-0'></ArrowLeft>
            <span className='align-middle d-sm-inline-block d-none'>Previous</span>
          </Button>
          <Button.Ripple type="submit" color="primary" disabled={isLoading}>
            {isLoading ? (
              <div className="spinner-border spinner-border-sm" role="status">
                {/* <span className="visually-hidden">Loading...</span> */}
              </div>
            ) : (
              <>
                Next <ArrowRight size={14} className="ml-25" />
              </>
            )}
          </Button.Ripple>
        </div>
      </Form>
    </Fragment>
  )
}

export default ProductDetails