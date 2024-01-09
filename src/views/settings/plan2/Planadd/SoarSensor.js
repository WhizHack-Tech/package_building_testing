// ================================================================================================
//  File Name: SoarSensor.js
//  Description: Details of the Setting ( Plan Add ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import axios from '@axios'
import { Fragment, useState } from 'react'
import { Card, CardBody, Row, Col, Input, Label, Button, Form } from 'reactstrap'
import Select from 'react-select'
import Flatpickr from 'react-flatpickr'
import { token, selectThemeColors } from '@utils'
import { ArrowLeft, ArrowRight } from 'react-feather'
import { useParams } from "react-router-dom"
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../../constants/api_message'
// import api_msg from "../../../constants/api_message"
const MySwal = withReactContent(Swal)

let planId = ''
const serchState = () => {
    const searchParams = new URLSearchParams(window.location.search)
    planId = searchParams.get('plan_id')
}

const Soar = () => {
    const [traceOptions, setTraceOptions] = useState([])
    const [startDate, setStartDate] = useState(new Date())
    const [endDate, setEndDate] = useState(new Date())
    const [isLoading, setIsLoading] = useState(false)
    const onSubmit = (event) => {
        event.preventDefault()
        serchState()
        setIsLoading(true)

        const bodyFormData = new FormData(event.target)
        bodyFormData.append("plan_id", planId)

        axios("/add-soar-license-plan-step-three", {
            method: "post",
            data: bodyFormData,
            headers: { Authorization: token() }
        })
            .then(res => {
                setIsLoading(false)
                if (res.data.message_type === 'successfully_inserted') {
                    MySwal.fire({
                        title: api_msg.title_msg,
                        text: 'Sit Back and Relax',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary'
                        },
                        buttonsStyling: false
                    })
                } else if (res.data.message_type === "unsuccessful") {
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
                setIsLoading(false)
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
            <Form onSubmit={onSubmit}>
                <Row>
                    <div className='content-header col-12 mt-2'>
                        <h5 className='mb-0'>SOAR</h5>
                        <hr />
                    </div>
                    <Col sm='3'>
                        <Label>Control Server Domain</Label>

                        <Input type='text' name='control_server_domain' required />

                    </Col>

                    {/* <Col sm='3'>

                        <Label>Control Server Port</Label>

                        <Input type='text' name='control_server_port' required />

                    </Col> */}

                    <Col sm='3'>

                        <Label>Aggregator Port</Label>

                        <Input type='text' name='aggregator_port' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Aggregator Domain</Label>

                        <Input type='text' name='aggregator_domain' required />

                    </Col>
                    <Col sm='3'>

                        <Label>Sensor Type</Label>

                        <Input type='select' name='sensor_type' required>

                            <option value="" selected disabled>--Select--</option>
                            <option value="NIDS">NIDS</option>
                            <option value='TRACE'>TRACE</option>
                            <option value='HIDS'>HIDS</option>
                            <option value='SOAR'>SOAR</option>


                        </Input>

                    </Col>

                    <Col sm='3'>

                        <Label>Registry Address</Label>

                        <Input type='text' name='registry_address' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Access Id</Label>

                        <Input type='text' name='access_id' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Access Key</Label>

                        <Input type='text' name='access_key' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Edition</Label>

                        <Input type='text' name='edition' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Location</Label>

                        <Input type='text' name='location' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Client City</Label>

                        <Input type='text' name='client_city' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Client Latitude</Label>

                        <Input type='text' name='client_latitude' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Client Longitude</Label>

                        <Input type='text' name='client_longitude' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Client Country Code</Label>

                        <Input type='text' name='client_country_code' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Client Country Name</Label>

                        <Input type='text' name='client_country_name' required />

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

                        <Input type='select' name='xdr_soar_status' required>

                            <option value="active" selected disabled>--Select--</option>

                            <option value="active">Active</option>

                            <option value="deactive">Inactive</option>
                        </Input>

                    </Col>
                    {/*
                    <Col sm='3'>

                        <Label>Current Sensor Status</Label>

                        <Input type='select' name='xdr_hids_manager_status' required>

                            <option value="active" selected disabled>--Select--</option>

                            <option value="active">Active</option>

                            <option value="deactive">Inactive</option>

                        </Input>

                    </Col> */}

                    <Col sm='3'>

                        <Label>XDR default Region</Label>

                        <Input type='text' name='aws_default_region' required />

                    </Col>

                    {/* <Col sm='3'>

                        <Label>Data Sharing Mode</Label>

                        <Input type='select' name='data_sharing_mode' required>

                            <option value="enable" selected disabled>--Select--</option>

                            <option value="enabled">Enabled</option>

                            <option value="disabled">Disabled</option>

                        </Input>

                    </Col> */}
                    <Col sm='3'>

                        <Label>Operating Env</Label>

                        <Input type='select' name='operating_env' required>

                            <option value="asw" selected disabled>--Select--</option>

                            <option value="aws">AWS</option>

                            <option value="azure">Azure</option>

                            <option value="onprim">On-Prim</option>

                        </Input>

                    </Col>

                    <Col sm='3'>

                        <Label>SOAR Sensor Host URL</Label>

                        <Input type='text' name='soar_sensor_host_url' required />

                    </Col>

                    {/* <Col sm='3'>

                        <Label>Preferred INT</Label>

                        <Input type='text' name='preferred_int' required />

                    </Col> */}

                    {/* <Col sm='3'>

                        <Label>SOAR Sensor Count</Label>

                        <Input type='text' name='sensor_count' required />

                    </Col> */}

                    <Col sm='3'>

                        <Label>SOAR Sensor Create Count</Label>

                        <Input type='text' name='sensor_create_count' required />

                    </Col>
                    <Col sm='3'>

                        <Label>Backend Port</Label>

                        <Input type='text' name='backend_port' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Frontend Port</Label>

                        <Input type='text' name='frontend_port' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Frontend Port HTTPS</Label>

                        <Input type='text' name='frontend_port_https' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Shuffle Default Username</Label>

                        <Input type='text' name='shuffle_default_username' required />

                    </Col>

                    <Col sm='3'>

                        <Label>Shuffle Default Password</Label>

                        <Input type='text' name='shuffle_default_password' required />

                    </Col>

                    <Col sm='3'>

                        <Label>shuffle Default Apikey</Label>

                        <Input type='text' name='shuffle_default_apikey' />

                    </Col>

                </Row>

                <div className='d-flex justify-content-end mt-2'>

                    <Button.Ripple type="submit" color="primary" disabled={isLoading}>

                        {isLoading ? (

                            <div className="spinner-border spinner-border-sm" role="status">

                            </div>

                        ) : (

                            <>

                                Submit

                            </>
                        )}

                    </Button.Ripple>

                </div>

            </Form>

        </Fragment>

    )
}

export default Soar