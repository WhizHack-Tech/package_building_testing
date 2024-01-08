// ================================================================================================
//  File Name: Nidslisence.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import { useEffect, useState } from 'react'
import { useParams } from "react-router-dom"
import axios from '@axios'
import { token } from '@utils'
import { Card, CardTitle, Label, Col, Input, Row, Button, Spinner, Form } from 'reactstrap'
import "./Loader.css"
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../../constants/api_message'
import Flatpickr from 'react-flatpickr'

const MySwal = withReactContent(Swal)
const Lisence = () => {
  const { id, activated_plan_id } = useParams()
  const [loading, setLoading] = useState(false)
  const [apiData, setApiData] = useState([])
  const [startDate, setStartDate] = useState(new Date())
  const [endDate, setEndDate] = useState(new Date())
  const [apiLoading, setApiLoading] = useState(false)

  const apiCall = () => {
    setApiLoading(true)
    axios.get(`/display-nids-license-management?location_id=${id}&activated_plan_id=${activated_plan_id}`, { headers: { Authorization: token() } }).then(res => {
      if (res.data.message_type === 'success') {
        setApiData(res.data.data[0])
        setStartDate(res.data.data[0].license_start_date)
        setEndDate(res.data.data[0].license_end_date)
      }
      setApiLoading(false)
    }).catch(e => {
      setApiLoading(false)
    })
  }

  useEffect(() => {
    apiCall()
  }, [])

  const lisenceUpdateForm = (event) => {
    setLoading(true)
    event.preventDefault()
    const bodyFormData = new FormData(event.target)

    axios({
      method: 'post',
      url: `/display-nids-license-management?activated_plan_id=${activated_plan_id}`,
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
        } else if (res.data.message_type === 'd_not_f') {
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
          <div class="tri-color-ripple-spinner">
            <div class="ripple ripple1"></div>
            <div class="ripple ripple2"></div>
          </div>
        </div>
      ) : (
        <Form onSubmit={lisenceUpdateForm}>
           <Row>
          <div className='content-header col-12 mt-2'>
            <h5 className='mb-0'>NIDS</h5>
            <hr />
          </div>
          <Col sm='3'>
            <Label>Control Server Domain</Label>

            <Input type='text' name='control_server_domain' defaultValue={apiData.control_server_domain || ''} />

          </Col>

          {/* <Col sm='3'>

            <Label>Control Server Port</Label>

            <Input type='text' name='control_server_port' defaultValue={apiData.control_server_domain || ''} />

          </Col> */}

          <Col sm='3'>

            <Label>Aggregator Port</Label>

            <Input type='text' name='aggregator_port' defaultValue={apiData.aggregator_port || ''} />

          </Col>

          <Col sm='3'>

            <Label>Aggregator Domain</Label>

            <Input type='text' name='aggregator_domain' defaultValue={apiData.aggregator_domain || ''} />

          </Col>

          <Col sm='3'>

            <Label>Sensor Type</Label>

            <Input type='select' name='sensor_type'>

              <option value="" selected disabled>{apiData.sensor_type || ''}</option>
              <option value="NIDS">NIDS</option>
              <option value='TRACE'>TRACE</option>
              <option value='HIDS'>HIDS</option>
              <option value='SOAR'>SOAR</option>

            </Input>

          </Col>

          <Col sm='3'>

            <Label>Registry Address</Label>

            <Input type='text' name='registry_address' defaultValue={apiData.registry_address || ''} />

          </Col>

          <Col sm='3'>

            <Label>Access Id</Label>

            <Input type='text' name='access_id' defaultValue={apiData.access_id || ''} />

          </Col>

          <Col sm='3'>

            <Label>Access Key</Label>

            <Input type='text' name='access_key' defaultValue={apiData.access_key || ''} />

          </Col>

          <Col sm='3'>

            <Label>Edition</Label>

            <Input type='text' name='edition' defaultValue={apiData.edition || ''} />

          </Col>

          <Col sm='3'>

            <Label>Location</Label>

            <Input type='text' name='location' defaultValue={apiData.location || ''} />

          </Col>

          <Col sm='3'>

            <Label>Client City</Label>

            <Input type='text' name='client_city' defaultValue={apiData.client_city || ''} />

          </Col>

          <Col sm='3'>

            <Label>Client Latitude</Label>

            <Input type='text' name='client_latitude' defaultValue={apiData.client_latitude || ''} />

          </Col>

          <Col sm='3'>

            <Label>Client Longitude</Label>

            <Input type='text' name='client_longitude' defaultValue={apiData.client_longitude || ''} />

          </Col>

          <Col sm='3'>

            <Label>Client Country Code</Label>

            <Input type='text' name='client_country_code' defaultValue={apiData.client_country_code || ''} />

          </Col>

          <Col sm='3'>

            <Label>Client Country Name</Label>

            <Input type='text' name='client_country_name' defaultValue={apiData.client_country_name || ''} />

          </Col>

          <Col sm='3'>

            <Label for="start_date_label">License Start Date</Label>

            <Flatpickr

              className='form-control'

              value={startDate}

              id='start_date_label'

              onChange={date => setStartDate(date)}

              name='license_start_date'

              options={{
                dateFormat: 'Y-m-d' // Set the date format to DD-MM-YY
              }}
            />

          </Col>

          <Col sm='3'>

            <Label for="end_date_label">License End Date</Label>

            <Flatpickr

              className='form-control'

              value={endDate}

              id='end_date_label'

              onChange={date => setEndDate(date)}

              name='license_end_date'
              
              options={{
                dateFormat: 'Y-m-d' // Set the date format to DD-MM-YY
              }}

            />

          </Col>

          <Col sm='3'>

            <Label>XDR NIDS Status</Label>

            <Input type='select' name='xdr_nids_status'>

              <option value="active" selected disabled>{apiData.xdr_nids_status || ''}</option>

              <option value="active" >Active</option>

              <option value="deactive">Inactive</option>

            </Input>

          </Col>

          {/* <Col sm='3'>

            <Label>Current Sensor Status</Label>

            <Input type='select' name='current_sensor_status' defaultValue={apiData.control_server_domain || ''}>

              <option value="active" selected disabled>--Select--</option>

              <option value="active" >Active</option>

              <option value="deactive">Inactive</option>

            </Input>

          </Col> */}

          <Col sm='3'>

            <Label>XDR default Region</Label>

            <Input type='text' name='aws_default_region' defaultValue={apiData.aws_default_region || ''} />

          </Col>

          <Col sm='3'>

            <Label>Data Sharing Mode</Label>

            <Input type='select' name='data_sharing_mode'>

              <option value="enable" selected disabled>{apiData.data_sharing_mode || ''}</option>

              <option value="enabled">Enabled</option>

              <option value="disabled">Disabled</option>

            </Input>

          </Col>

          <Col sm='3'>

            <Label>Operating Env</Label>

            <Input type='select' name='operating_env'>

              <option value="asw" selected disabled>{apiData.operating_env || ''}</option>

              <option value="aws">AWS</option>

              <option value="azure">Azure</option>

              <option value="onprim">On-Prim</option>

            </Input>

          </Col>

          {/* <Col sm='3'>

            <Label>NIDS Sensor Count</Label>

            <Input type='text' name='sensor_count' defaultValue={apiData.control_server_domain || ''} />

          </Col> */}

          <Col sm='3'>

            <Label>NIDS Sensor Create Count</Label>

            <Input type='number' name='sensor_create_count' defaultValue={apiData.sensor_create_count || ''} />

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
        </Form>)}
    </Card >
  )
}

export default Lisence
