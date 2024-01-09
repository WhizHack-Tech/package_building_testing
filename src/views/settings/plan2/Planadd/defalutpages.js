// ================================================================================================
//  File Name: defalutpages.js
//  Description: Details of the Setting ( Plan Add ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// Import the necessary libraries
import React, { useState, useEffect, Fragment } from 'react'
import { useHistory } from 'react-router-dom'
import { Form, Label, Input, CustomInput, Col, Button, FormGroup, Row, Card } from 'reactstrap'
import styled from 'styled-components'
import axios from '@axios'
import Swal from 'sweetalert2'
// import api_msg from "../../../constants/api_message"
import api_msg from "../../../../constants/api_message"
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
let planid = ''

const serchState = () => {
  const searchParams = new URLSearchParams(window.location.search)
  const plan_id = searchParams.get('plan_id')
  planid = plan_id
  console.log({ planid })
}

const ProductDetails = ({ stepper }) => {
  const [isLoading, setIsLoading] = useState(false)
  const [default_page, setDefault_page] = useState('/dashboard/dashboard')
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

  const history = useHistory()

  const handleSubmit = (event) => {
    setIsLoading(true)
    serchState()
    event.preventDefault()

    // Prepare the data to be sent
    const bodyFormData = new FormData()
    bodyFormData.append('default_page', default_page)
    bodyFormData.append('env_nids', env_nids)
    bodyFormData.append('env_hids', env_hids)
    // bodyFormData.append('env_wazuh', env_wazuh)
    bodyFormData.append('env_trace', env_trace)
    bodyFormData.append('plan_id', planid)
    bodyFormData.append('xdr_live_map', live_map)

    bodyFormData.append('env_soar', envSoar)
    bodyFormData.append('env_hc', healthCheck)
    bodyFormData.append('env_mm', mediaManagement)
    bodyFormData.append('env_tptf', tpThreadFeed)
    bodyFormData.append('env_sbs', sandBox)
    bodyFormData.append('env_ess', ess)
    bodyFormData.append('env_tps', tpSource)


    // Make the POST request using Axios
    axios
      .post('/add-plan-step-two', bodyFormData, { headers: { Authorization: token() } })
      .then((response) => {
        setIsLoading(false)
        if (response.data.message_type === 'successfully_inserted') {
          stepper.next()
          if (response.data.message_type === "successfully_inserte") {
            Swal.fire({
              title: api_msg.title_msg,
              text: 'Sit Back and Relax',
              icon: 'success',
              customClass: {
                confirmButton: 'btn btn-primary'
              },
              buttonsStyling: false

            })

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
    <Card>
      <Fragment>
        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Col sm='2'>
              <Label>Default Page</Label>
              <Input
                type='select'
                value={default_page}
                onChange={(e) => setDefault_page(e.target.value)}
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
    </Card>
  )
}

export default ProductDetails