// ================================================================================================
//  File Name: Notification.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import { useState, useEffect } from 'react'
import { CustomInput, Button, Card, ModalBody, ModalFooter, Label, FormGroup, Input, Col, Row, Spinner, Form } from 'reactstrap'
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../../constants/api_message"
import { FormattedMessage } from 'react-intl'
import Select from 'react-select'
import { useParams } from 'react-router-dom'
import "./Loader.css"
const MySwal = withReactContent(Swal)
const NotificationsTabContent = () => {
  const [btnLoader, setBtnLoader] = useState(false)
  const [pageLoad, setPageLoad] = useState(false)
  const [data, setData] = useState([])
  const [platformVal, platformValSet] = useState([])
  const [severityVal, severityValSet] = useState([])
  const [traceVal, traceValSet] = useState([])
  const { id, activated_plan_id } = useParams()

  const platform = [
    { value: 'aws', label: 'Aws', color: '#00B8D9', isFixed: true },
    { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
    { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
  ]
  const severity = [
    { value: '1', label: 'High', color: '#00B8D9' },
    { value: '2', label: 'Medium', color: '#0052CC' },
    { value: '3', label: 'Low', color: '#5243AA' }
  ]
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

  const find_val_platform = (defaultValParam) => {

    let defaultVal = defaultValParam?.platform_val
    let finalData = []
    if (defaultVal !== undefined) {
      defaultVal = defaultVal.split(",")
      for (let p = 0; p < Object.keys(platform).length; p++) {
        for (let i = 0; i < defaultVal.length; i++) {
          if (platform[p].value === defaultVal[i]) {
            finalData.push(platform[p])
          }
        }
      }
    }

    return finalData
  }

  const find_val_severity = (defaultValParam) => {

    let defaultVal = defaultValParam?.severity_val
    let finalData = []
    if (defaultVal !== undefined) {
      defaultVal = defaultVal.split(",")
      for (let p = 0; p < Object.keys(severity).length; p++) {
        for (let i = 0; i < defaultVal.length; i++) {
          if (severity[p].value === defaultVal[i]) {
            finalData.push(severity[p])
          }
        }
      }
    }

    return finalData
  }

  const find_val_trace = (defaultValParam) => {

    let defaultVal = defaultValParam?.trace_sensor
    let finalData = []
    if (defaultVal && typeof defaultVal === 'string') {
      defaultVal = defaultVal.split(",")
      for (let p = 0; p < Object.keys(trace).length; p++) {
        for (let i = 0; i < defaultVal.length; i++) {
          if (trace[p].value === defaultVal[i]) {
            finalData.push(trace[p])
          }
        }
      }
    }

    return finalData
  }

  useEffect(() => {
    setPageLoad(true)
    axios.get(`/all-config?config_type=notification_live&location_id=${id}&activated_plan_id=${activated_plan_id}`, { headers: { Authorization: token() } }).then(
      res => {
        if (res.data.message_type === "data_found") {
          setData(res.data.data[0])
          platformValSet(find_val_platform(res.data.data[0]))
          severityValSet(find_val_severity(res.data.data[0]))
          traceValSet(find_val_trace(res.data.data[0]))
          setPageLoad(false)
        }
      }
    )

  }, [])

  const url_link = "/add-notification-config-update"
  function submit_form(event) {
    setBtnLoader(true)
    event.preventDefault()

    const bodyFormData = new FormData(event.target)
    bodyFormData.append("config_type", "notification_live")
    bodyFormData.append("location_id", id)
    bodyFormData.append("activated_plan_id", activated_plan_id)

    axios({
      method: "post",
      url: url_link,
      data: bodyFormData,
      headers: { Authorization: token() }

    })
      .then((res) => {
        setBtnLoader(false)
        if (res.data.message_type === "updated successfully") {
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
        setBtnLoader(false)
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

  if (pageLoad) {
    return (
      <div className='d-flex justify-content-center'>
         <div class="tri-color-ripple-spinner">
            <div class="ripple ripple1"></div>
            <div class="ripple ripple2"></div>
          </div>
      </div>
    )
  }

 
  if (!data || !data.accuracy_val) {
    return <div className='d-flex justify-content-center'>Data not found</div>
  }


  return (
    <Card>
      <Form onSubmit={submit_form}>
        <Row>
          {/* <Col sm='6'>
              <FormGroup>
                <Label><FormattedMessage id='Email' /></Label>
                <Input type='text' name="email_ids" defaultValue={data.email_ids} />
              </FormGroup>
            </Col> */}
          <Col className='mb-1' md='6' sm='12'>
            <Label><FormattedMessage id='Platform' /></Label>
            <Select
              isClearable={false}
              theme={selectThemeColors}
              isMulti
              name='platform_val[]'
              options={platform}
              defaultValue={platformVal}
              className='react-select'
              classNamePrefix='select'
            />
          </Col>
          {/* <Col className='mb-1' md='6' sm='12'>
            <Label><FormattedMessage id='Threat Severity' /></Label>
            <Select
              isClearable={false}
              theme={selectThemeColors}
              defaultValue={severityVal}
              isMulti
              name='severity_val[]'
              options={severity}
              className='react-select'
              classNamePrefix='select'
            />
          </Col> */}
          {/* <Col className='mb-1' md='6' sm='12'>
            <FormGroup>
              <Label>
                Accuray
              </Label>
              <Input type='select' name='accuracy_val'>
                <option value='1' selected={(data?.accuracy_val === 1)}>Between 91% to 100%</option>
                <option value='2' selected={(data?.accuracy_val === 2)}>Between 76% to 90%</option>
                <option value='3' selected={(data?.accuracy_val === 3)}>Between 65% to 75%</option>
              </Input>
            </FormGroup>
          </Col> */}
          <Col sm='6'>
            <FormGroup>
              <Label for='user-role'><FormattedMessage id='Time Interval' /></Label>
              <Input type='select' name='time_interval_val'>
                <option value='1' selected={(data?.time_interval_val === 1)}>Last 1 minutes</option>
                <option value='2' selected={(data?.time_interval_val === 2)}>Last 2 minutes</option>
                <option value='5' selected={(data?.time_interval_val === 5)}>Last 5 minutes</option>
                <option value='15' selected={(data?.time_interval_val === 15)}>Last 15 minutes</option>
                <option value='30' selected={(data?.time_interval_val === 30)}>Last 30 minutes</option>
                <option value='60' selected={(data?.time_interval_val === 60)}>Last 1 hour</option>
                <option value='360' selected={(data?.time_interval_val === 360)}>Last 6 hours</option>
                <option value='720' selected={(data?.time_interval_val === 720)}>Last 12 hours</option>
                <option value='1440' selected={(data?.time_interval_val === 1440)}>Last 24 hours</option>
              </Input>
            </FormGroup>
          </Col>
          <Col className='mb-1' md='6' sm='12'>
            <Label><FormattedMessage id='Trace' /></Label>
            <Select
              isClearable={false}
              theme={selectThemeColors}
              defaultValue={traceVal}
              isMulti
              name='trace_sensor[]'
              options={trace}
              className='react-select'
              classNamePrefix='select'
            />
          </Col>
          {/* <Col Col className='mb-1' md='6' sm='12'>
              <FormGroup>
                <Label>
                trace
                </Label>
                <Input type='select' name='trace_sensor'>
                  <option value='1' selected={(data.trace_sensor === 1)}>Wazuh</option>
                  <option value='2' selected={(data.trace_sensor === 2)}>NIDS</option>
                  <option value='3' selected={(data.trace_sensor === 3)}>HIDS</option>
                </Input>
              </FormGroup>
            </Col> */}
          <Col className='mt-1 d-flex justify-content-end' sm='12' >
            {btnLoader === false ? (
              <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'>
                <FormattedMessage id='Submit' />
              </Button.Ripple>
            ) : (
              <Button.Ripple color='success' className='btn-submit' type='submit'>
                <Spinner size='sm' />
                &nbsp;
                <FormattedMessage id='Saving' />
              </Button.Ripple>
            )}
          </Col>
        </Row>
      </Form>
    </Card>
  )
}

export default NotificationsTabContent