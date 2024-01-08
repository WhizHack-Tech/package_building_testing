// ================================================================================================
//  File Name: SoarSensor.js
//  Description: Details of the Setting ( Edit Plan ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================

import { useEffect, useState, Fragment } from 'react'
import { useParams } from "react-router-dom"
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import { Card, CardTitle, Label, Col, Input, Row, Button, Spinner, Form } from 'reactstrap'
import "./Loader.css"
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../constants/api_message'
import Flatpickr from 'react-flatpickr'
import Select from 'react-select'
import "flatpickr/dist/flatpickr.css"
import "flatpickr/dist/themes/dark.css"
const MySwal = withReactContent(Swal)


const Soar = () => {

  const [startDate, setStartDate] = useState(new Date())
  const [endDate, setEndDate] = useState(new Date())
  const [isLoading, setIsLoading] = useState(false)
  const [soarData, setSoarData] = useState('')
  const [loading, setLoading] = useState(false)
  const [apiLoading, setApiLoading] = useState(false)
  const { id } = useParams()

  const apiCall = () => {
    setApiLoading(true)
    axios.get(`/display-updated-plan/${id}/`, { headers: { Authorization: token() } }).then(res => {

        if (res.data.message_type === 'success') {
            setSoarData(res.data.data.soar_license_management)

            const licenseStartDate = res.data.data.soar_license_management.license_start_date
            if (licenseStartDate) {
                const [day, month, year] = licenseStartDate.split("-")
                const formattedEndDate = new Date(`${year}/${month}/${day}`)
                setStartDate(formattedEndDate)
            }

            const licenseEndDate = res.data.data.soar_license_management.license_end_date
            if (licenseEndDate) {
                const [day, month, year] = licenseEndDate.split("-")
                const formattedEndDate = new Date(`${year}/${month}/${day}`)
                setEndDate(formattedEndDate)
            }

            setTraceOptions(findValOption(res.data.data.soar_license_management.sensor_name, trace))
            console.log("Date formate", res.data.data.soar_license_management.license_start_date)

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
        url: `/soar-license-update-details-plan2?plan_id=${id}`,
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

    <Fragment>
     {apiLoading ? (
                <div className='d-flex justify-content-center'>
                    <div class="tri-color-ripple-spinner">
                        <div class="ripple ripple1"></div>
                        <div class="ripple ripple2"></div>
                    </div>
                </div>
            ) : (<Form onSubmit={lisenceUpdateForm}>
       <Row>
                        <div className='content-header col-12 mt-2'>
                            <h5 className='mb-0'>SOAR</h5>
                            <hr />
                        </div>
                        <Col sm='3'>
                            <Label>Control Server Domain</Label>

                            <Input type='text' name='control_server_domain' defaultValue={soarData.control_server_domain || ''} />

                        </Col>

                        {/* <Col sm='3'>

                        <Label>Control Server Port</Label>

                        <Input type='text' name='control_server_port' defaultValue={soarData.control_server_domain || ''} />

                    </Col> */}

                        <Col sm='3'>

                            <Label>Aggregator Port</Label>

                            <Input type='text' name='aggregator_port' defaultValue={soarData.aggregator_port || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Aggregator Domain</Label>

                            <Input type='text' name='aggregator_domain' defaultValue={soarData.aggregator_domain || ''} />

                        </Col>
                        <Col sm='3'>

                            <Label>Sensor Type</Label>

                            <Input type='select' name='sensor_type'>

                                <option value="" selected disabled>{soarData.sensor_type || ''}</option>
                                <option value="NIDS">NIDS</option>
                                <option value='TRACE'>TRACE</option>
                                <option value='HIDS'>HIDS</option>
                                <option value='SOAR'>SOAR</option>


                            </Input>

                        </Col>

                        <Col sm='3'>

                            <Label>Registry Address</Label>

                            <Input type='text' name='registry_address' defaultValue={soarData.registry_address || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Access Id</Label>

                            <Input type='text' name='access_id' defaultValue={soarData.access_id || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Access Key</Label>

                            <Input type='text' name='access_key' defaultValue={soarData.access_key || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Edition</Label>

                            <Input type='text' name='edition' defaultValue={soarData.edition || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Location</Label>

                            <Input type='text' name='location' defaultValue={soarData.location || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Client City</Label>

                            <Input type='text' name='client_city' defaultValue={soarData.client_city || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Client Latitude</Label>

                            <Input type='text' name='client_latitude' defaultValue={soarData.client_latitude || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Client Longitude</Label>

                            <Input type='text' name='client_longitude' defaultValue={soarData.client_longitude || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Client Country Code</Label>

                            <Input type='text' name='client_country_code' defaultValue={soarData.client_country_code || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Client Country Name</Label>

                            <Input type='text' name='client_country_name' defaultValue={soarData.client_country_name || ''} />

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
                                    dateFormat: 'd-m-Y' // Set the date format to DD-MM-YY
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
                                    dateFormat: 'd-m-Y' // Set the date format to DD-MM-YY
                                }}

                            />

                        </Col>

                        <Col sm='3'>

                            <Label>XDR SOAR Status</Label>

                            <Input type='select' name='xdr_soar_status'>

                                <option value="active" selected disabled>{soarData.xdr_soar_status || ''}</option>

                                <option value="active">Active</option>

                                <option value="deactive">Inactive</option>
                            </Input>

                        </Col>
                        {/* 
                    <Col sm='3'>

                        <Label>Current Sensor Status</Label>

                        <Input type='select' name='xdr_hids_manager_status' defaultValue={soarData.control_server_domain || ''}>

                            <option value="active" selected disabled>{soarData.control_server_domain || ''}</option>

                            <option value="active">Active</option>

                            <option value="deactive">Inactive</option>

                        </Input>

                    </Col> */}

                        <Col sm='3'>

                            <Label>XDR default Region</Label>

                            <Input type='text' name='aws_default_region' defaultValue={soarData.aws_default_region || ''} />

                        </Col>

                        {/* <Col sm='3'>

                            <Label>Data Sharing Mode</Label>

                            <Input type='select' name='data_sharing_mode'>

                                <option value="enable" selected disabled>{soarData.data_sharing_mode || ''}</option>

                                <option value="enabled">Enabled</option>

                                <option value="disabled">Disabled</option>

                            </Input>

                        </Col> */}
                        <Col sm='3'>

                            <Label>Operating Env</Label>

                            <Input type='select' name='operating_env'>

                                <option value="asw" selected disabled>{soarData.operating_env || ''}</option>

                                <option value="aws">AWS</option>

                                <option value="azure">Azure</option>

                                <option value="onprim">On-Prim</option>

                            </Input>

                        </Col>

                        <Col sm='3'>

                            <Label>SOAR Sensor Host URL</Label>

                            <Input type='text' name='soar_sensor_host_url' defaultValue={soarData.soar_sensor_host_url || ''} />

                        </Col>
{/* 
                        <Col sm='3'>

                            <Label>Preferred INT</Label>

                            <Input type='text' name='preferred_int' defaultValue={soarData.preferred_int || ''} />

                        </Col> */}

                        {/* <Col sm='3'>

                        <Label>SOAR Sensor Count</Label>

                        <Input type='text' name='sensor_count' defaultValue={soarData.control_server_domain || ''} />

                    </Col> */}

                        <Col sm='3'>

                            <Label>SOAR Sensor Create Count</Label>

                            <Input type='number' name='sensor_create_count' defaultValue={soarData.sensor_create_count || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Backend Port</Label>

                            <Input type='text' name='backend_port' defaultValue={soarData.backend_port || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Frontend Port</Label>

                            <Input type='text' name='frontend_port' defaultValue={soarData.frontend_port || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Frontend Port HTTPS</Label>

                            <Input type='text' name='frontend_port_https' defaultValue={soarData.frontend_port_https || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Shuffle Default Username</Label>

                            <Input type='text' name='shuffle_default_username' defaultValue={soarData.shuffle_default_username || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>Shuffle Default Password</Label>

                            <Input type='text' name='shuffle_default_password' defaultValue={soarData.shuffle_default_password || ''} />

                        </Col>

                        <Col sm='3'>

                            <Label>shuffle Default Apikey</Label>

                            <Input type='text' name='shuffle_default_apikey' defaultValue={soarData.shuffle_default_apikey || ''} />

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

    </Fragment>

  )
}

export default Soar