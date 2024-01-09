// ================================================================================================
//  File Name: traceLicense.js
//  Description: Details of the Setting ( Edit Plan ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import { useEffect, useState } from 'react'
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

const trace = [
    { value: 'database-server', label: 'Database Server', color: '#5243AA', isFixed: true },
    { value: 'dicom-server', label: 'Dicom Server', color: '#5243AA', isFixed: true },
    { value: 'dns-server', label: 'DNS Server', color: '#5243AA', isFixed: true },
    { value: 'ftp-server', label: 'FTP Server', color: '#5243AA', isFixed: true },
    { value: 'gas-station', label: 'Gas Station', color: '#5243AA', isFixed: true },
    { value: 'industrial', label: 'Industrial', color: '#5243AA', isFixed: true },
    { value: 'it-ot-gateway', label: 'IT-OT Gateway', color: '#5243AA', isFixed: true },
    { value: 'mail-server', label: 'Email Server', color: '#5243AA', isFixed: true },
    { value: 'plc-s71200', label: 'PLC Sensor (S7-1200)', color: '#5243AA', isFixed: true },
    { value: 'plc-s71500', label: 'PLC Sensor (S7-1500)', color: '#5243AA', isFixed: true },
    { value: 'plc-s7300', label: 'PLC Sensor (S7-7300)', color: '#5243AA', isFixed: true },
    { value: 'proxy-server', label: 'Proxy Server', color: '#5243AA', isFixed: true },
    { value: 'quicksand', label: 'Quicksand', color: '#5243AA', isFixed: true },
    { value: 'remote-workspaces', label: 'Remote-Workspace', color: '#5243AA', isFixed: true },
    { value: 'shellcode-extractor', label: 'Shellcode Extractor', color: '#5243AA', isFixed: true },
    { value: 'smart-grid', label: 'Smart Grid', color: '#5243AA', isFixed: true },
    { value: 'web-application', label: 'Web Application Server', color: '#5243AA', isFixed: true }
]


const TraceLicense = () => {
    const { id } = useParams()
    const [loading, setLoading] = useState(false)
    const [apiLoading, setApiLoading] = useState(false)
    const [traceData, setTraceData] = useState([])
    const [traceOptions, setTraceOptions] = useState([])
    const [startDate, setStartDate] = useState("")
    const [endDate, setEndDate] = useState("")

    const findValOption = (defaultVal, compereList) => {
        let finalData = []
        if (defaultVal !== undefined) {
            defaultVal = defaultVal.split(",")
            for (let p = 0; p < Object.keys(compereList).length; p++) {
                for (let i = 0; i < defaultVal.length; i++) {
                    if (compereList[p].value === defaultVal[i]) {
                        finalData.push(compereList[p])
                    }
                }
            }
        }
        return finalData
    }

    const apiCall = () => {
        setApiLoading(true)
        axios.get(`/display-updated-plan/${id}/`, { headers: { Authorization: token() } }).then(res => {

            if (res.data.message_type === 'success') {
                setTraceData(res.data.data.trace_license_management)

                const licenseStartDate = res.data.data.trace_license_management.license_start_date
                if (licenseStartDate) {
                    const [day, month, year] = licenseStartDate.split("-")
                    const formattedEndDate = new Date(`${year}/${month}/${day}`)
                    setStartDate(formattedEndDate)
                }

                const licenseEndDate = res.data.data.trace_license_management.license_end_date
                if (licenseEndDate) {
                    const [day, month, year] = licenseEndDate.split("-")
                    const formattedEndDate = new Date(`${year}/${month}/${day}`)
                    setEndDate(formattedEndDate)
                }

                setTraceOptions(findValOption(res.data.data.trace_license_management.sensor_name, trace))

            }
            setApiLoading(false)
        }).catch(e => {
            setApiLoading(false)
        })
    }

    useEffect(() => {
        apiCall()
    }, [])


    console.log(startDate)

    const lisenceUpdateForm = (event) => {
        setLoading(true)
        event.preventDefault()
        const bodyFormData = new FormData(event.target)

        axios({
            method: 'post',
            url: `/trace-license-update-details-plan2?plan_id=${id}`,
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
        <Card>
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
                        <h5 className='mb-0'>TRACE</h5>
                        <hr />
                    </div>
                    <Col sm='3'>
                        <Label>Control Server Domain</Label>

                        <Input type='text' name='control_server_domain' defaultValue={traceData.control_server_domain || ''} />

                    </Col>

                    {/* <Col sm='3'>

                        <Label>Control Server Port</Label>

                        <Input type='text' name='control_server_port' />

                    </Col> */}

                    <Col sm='3'>

                        <Label>Aggregator Port</Label>

                        <Input type='text' name='aggregator_port' defaultValue={traceData.control_server_domain || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Aggregator Domain</Label>

                        <Input type='text' name='aggregator_domain' defaultValue={traceData.aggregator_domain || ''} />

                    </Col>

                    {/* <Col sm='3'>

                        <Label>Sensor Access Id</Label>

                        <Input type='text' name='sensor_access_id' />

                    </Col> */}
                    {/*
                    <Col sm='3'>

                        <Label>Sensor Password</Label>

                        <Input type='text' name='sensor_password' />

                    </Col> */}

                    <Col sm='3'>

                        <Label>Sensor Type</Label>

                        <Input type='select' name='sensor_type' >

                            <option value="" selected disabled>{traceData.sensor_type || ''}</option>
                            <option value="NIDS">NIDS</option>
                            <option value='TRACE'>TRACE</option>
                            <option value='HIDS'>HIDS</option>
                            <option value='SOAR'>SOAR</option>


                        </Input>

                    </Col>

                    <Col sm='3'>

                        <Label>Registry Address</Label>

                        <Input type='text' name='registry_address' defaultValue={traceData.registry_address || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Access Id</Label>

                        <Input type='text' name='access_id' defaultValue={traceData.access_id || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Access Key</Label>

                        <Input type='text' name='access_key' defaultValue={traceData.access_key || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Edition</Label>

                        <Input type='text' name='edition' defaultValue={traceData.edition || ''} />

                    </Col>

                    <Col sm='3'>
                        <Label for="sensor_name_id">Sensor Name</Label>
                        <Select
                            id="sensor_name_id"
                            isClearable={false}
                            theme={selectThemeColors}
                            isMulti
                            name='sensor_name[]'
                            options={trace}
                            defaultValue={traceOptions}
                            className='react-select'
                            classNamePrefix='select'
                        />
                    </Col>

                    <Col sm='3'>

                        <Label>Location</Label>

                        <Input type='text' name='location' defaultValue={traceData.location || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Client City</Label>

                        <Input type='text' name='client_city' defaultValue={traceData.client_city || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Client Latitude</Label>

                        <Input type='text' name='client_latitude' defaultValue={traceData.client_latitude || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Client Longitude</Label>

                        <Input type='text' name='client_longitude' defaultValue={traceData.client_longitude || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Client Country Code</Label>

                        <Input type='text' name='client_country_code' defaultValue={traceData.client_country_code || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Client Country Name</Label>

                        <Input type='text' name='client_country_name' defaultValue={traceData.client_country_name || ''} />

                    </Col>

                    {/* <Col sm='3'>

                        <Label>Honeynet Interface</Label>

                        <Input type='text' name='honeynet_interface' />

                    </Col> */}

                    {/* <Col sm='3'>

                        <Label>Enable Monitoring</Label>

                        <Input type='text' name='enable_monitoring' />

                    </Col> */}
                    {/*
                    <Col sm='3'>

                        <Label>Monitor Interface</Label>

                        <Input type='text' name='monitor_interface' />

                    </Col> */}

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

                        <Label>XDR Trace Status</Label>

                        <Input type='select' name='xdr_trace_status' >

                            <option value="active" selected disabled>{traceData.xdr_trace_status || ''}</option>

                            <option value="active" >Active</option>

                            <option value="deactive">Inactive</option>

                        </Input>

                    </Col>

                    <Col sm='3'>

                        <Label>Diss Status</Label>

                        <Input type='select' name='diss_status'>

                            <option selected disabled>{traceData.diss_status || ''}</option>
                            <option value="static">Static</option>
                            <option value="sequental">Sequental</option>
                            <option value="dynamic">Dynamic</option>

                        </Input>

                    </Col>

                    <Col sm='3'>

                        <Label>Diss Mode</Label>

                        <Input type='text' name='diss_mode' defaultValue={traceData.diss_mode || ''} />

                    </Col>

                    <Col sm='3'>

                        <Label>Data Sharing Mode</Label>

                        <Input type='select' name='data_sharing_mode' >

                            <option value="enable" selected disabled>{traceData.data_sharing_mode || ''}</option>

                            <option value="enabled">Enabled</option>

                            <option value="disabled">Disabled</option>

                        </Input>

                    </Col>
                    <Col sm='3'>

                        <Label>Operating Env</Label>

                        <Input type='select' name='operating_env' >

                            <option value="asw" selected disabled>{traceData.operating_env || ''}</option>

                            <option value="aws">AWS</option>

                            <option value="azure">Azure</option>

                            <option value="onprim">On-Prim</option>

                        </Input>

                    </Col>

                    <Col sm='3'>

                        <Label>TRACE Sensor Create Count</Label>

                        <Input type='number' name='sensor_create_count' defaultValue={traceData.sensor_create_count || ''} />

                    </Col>
                    <Col sm='3'>

                        <Label>XDR default Region</Label>

                        <Input type='text' name='aws_default_region' defaultValue={traceData.aws_default_region || ''} />

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
        </Card>
    )
}

export default TraceLicense
