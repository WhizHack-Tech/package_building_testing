// ================================================================================================
//  File Name: Dashboard.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect, Fragment } from 'react'
import { CustomInput, Button, Card, ModalBody, ModalFooter, Label, FormGroup, Input, Col, Row, Spinner, Form } from 'reactstrap'
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../constants/api_message"
import { useTranslation } from 'react-i18next'
import Select from 'react-select'
import { useSelector } from "react-redux"
const MySwal = withReactContent(Swal)
const NotificationsTabContent = () => {
  const { t } = useTranslation()
  const [btnLoader, setBtnLoader] = useState(false)
  const [pageLoad, setPageLoad] = useState(false)
  const [data, setData] = useState([])
  const [platformVal, platformValSet] = useState([])
  const [severityVal, severityValSet] = useState([])
  const [traceVal, traceValSet] = useState([])
  const pagePermissionStore = useSelector((store) => store.pagesPermissions)

  const platform = [
    { value: 'aws', label: 'AWS', color: '#00B8D9', isFixed: true },
    { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
    { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
  ]
  const severity = [
    { value: '1', label: 'High', color: '#00B8D9', isFixed: true },
    { value: '2', label: 'Medium', color: '#0052CC', isFixed: true },
    { value: '3', label: 'Low', color: '#5243AA', isFixed: true }
  ]

  const traceConfig = [
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
    let finalData = []

    if (defaultValParam.platform_val) {
      let defaultVal = defaultValParam.platform_val
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
    }

    return finalData
  }

  const find_val_severity = (defaultValParam) => {

    let finalData = []

    if (defaultValParam.severity_val) {
      let defaultVal = defaultValParam.severity_val
      if (defaultVal !== undefined) {
        defaultVal = defaultVal.split(",")
        for (let p = 0; p < Object.keys(platform).length; p++) {
          for (let i = 0; i < defaultVal.length; i++) {
            if (severity[p].value === defaultVal[i]) {
              finalData.push(severity[p])
            }
          }
        }
      }
    }

    return finalData
  }

  const find_val_trace = (defaultValParam) => {

    let finalData = []

    if (defaultValParam.trace_sensor) {
      let defaultVal = defaultValParam.trace_sensor
      if (defaultVal !== undefined) {
        defaultVal = defaultVal.split(",")
        for (let p = 0; p < Object.keys(traceConfig).length; p++) {
          for (let i = 0; i < defaultVal.length; i++) {
            if (traceConfig[p].value === defaultVal[i]) {
              finalData.push(traceConfig[p])
            }
          }
        }
      }
    }

    return finalData
  }

  useEffect(() => {
    setPageLoad(true)
    axios.get('/display-config?config_type=dashboard_filter', { headers: { Authorization: token() } }).then(
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

  const url_link = "/update-dashboard-config"
  function submit_form(event) {
    setBtnLoader(true)
    event.preventDefault()

    const bodyFormData = new FormData(event.target)
    bodyFormData.append("config_type", "dashboard_filter")

    axios({
      method: "post",
      url: url_link,
      data: bodyFormData,
      headers: { Authorization: token() }

    })
      .then((res) => {
        setBtnLoader(false)
        if (res.data.message_type === "updated") {
          MySwal.fire({
            title: api_msg.title_msg,
            text: 'Sit Back and Relax',
            icon: 'success',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
          })

        } else if (res.data.message_type === "form_errror") {
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
    return <div className='text-center'><Spinner color="primary" /></div>
  }

  return (
    <Fragment>
      <Form onSubmit={submit_form}>
        <Row>
          <Col className='mb-1' md='6' sm='12'>
            <Label>{t('Platform')}</Label>
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
            <Label>{t('Threat Severity')}</Label>
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
          <Col sm='6'>
            <FormGroup>
              <Label>{t('Accuracy')}</Label>
              <Input type='select' name='accuracy_val'>
                <option value='1' selected={(data.accuracy_val === 1)}>Between 91% to 100%</option>
                <option value='2' selected={(data.accuracy_val === 2)}>Between 76% to 90%</option>
                <option value='3' selected={(data.accuracy_val === 3)}>Between 65% to 75%</option>
              </Input>
            </FormGroup>
          </Col>
          {
            (pagePermissionStore.env_trace) ? <Col sm='6'>
              <FormGroup>
                <Label>Trace</Label>
                <Select
                  isClearable={false}
                  theme={selectThemeColors}
                  isMulti
                  isDisabled={true}
                  // name='trace_sensor[]'
                  options={traceConfig}
                  defaultValue={traceVal}
                  className='react-select'
                  classNamePrefix='select'
                />
              </FormGroup>
            </Col> : null
          }
          <Col sm='12'>
            <FormGroup>
              {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'>{t('Submit')}</Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' />&nbsp;{t('Saving')}...</Button.Ripple>}
            </FormGroup>
          </Col>
        </Row>
      </Form>
    </Fragment>
  )
}

export default NotificationsTabContent