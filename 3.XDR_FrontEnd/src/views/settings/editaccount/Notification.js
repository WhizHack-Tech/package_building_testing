// ================================================================================================
//  File Name: Notification.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect } from 'react'
import { CustomInput, Button, Card, ModalBody, ModalFooter, Label, FormGroup, Input, Col, Row, Spinner, Form } from 'reactstrap'
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../constants/api_message"
import { useTranslation } from 'react-i18next'
import Select from 'react-select'
const MySwal = withReactContent(Swal)
const NotificationsTabContent = () => {
  const { t } = useTranslation()
  const [btnLoader, setBtnLoader] = useState(false)
  const [pageLoad, setPageLoad] = useState(false)
  const [data, setData] = useState([])
  const [email, setEmail] = useState([])
  const [platformVal, platformValSet] = useState([])
  const [severityVal, severityValSet] = useState([])

  const platform = [
    { value: 'aws', label: 'AWS', color: '#00B8D9', isFixed: true },
    { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
    { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
  ]
  const severity = [
    { value: '1', label: 'High', color: '#00B8D9' },
    { value: '2', label: 'Medium', color: '#0052CC' },
    { value: '3', label: 'Low', color: '#5243AA' }
  ]

  const find_val_platform = (defaultValParam) => {

    let defaultVal = defaultValParam.platform_val
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

    let defaultVal = defaultValParam.severity_val
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

  useEffect(() => {
    setPageLoad(true)
    axios.get('/display-config?config_type=notification_live', { headers: { Authorization: token() } }).then(
      res => {
        if (res.data.message_type === "data_found") {
          setData(res.data.data[0])
          platformValSet(find_val_platform(res.data.data[0]))
          severityValSet(find_val_severity(res.data.data[0]))
          setPageLoad(false)
        }
      })

  }, [])

  const url_link = "/update-notification-config"
  function submit_form(event) {
    setBtnLoader(true)
    event.preventDefault()

    const bodyFormData = new FormData(event.target)
    bodyFormData.append("config_type", "notification_live")

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
    <Card>
      <Form onSubmit={submit_form}>
        <div style={{ height: '130px' }}>
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
                <Label for='user-role'>{t('Time Interval')}</Label>
                <Input type='select' name='time_interval_val'>
                  <option value='1' selected={(data.time_interval_val === 1)}>Last 1 minutes</option>
                  <option value='2' selected={(data.time_interval_val === 2)}>Last 2 minutes</option>
                  <option value='5' selected={(data.time_interval_val === 5)}>Last 5 minutes</option>
                  <option value='15' selected={(data.time_interval_val === 15)}>Last 15 minutes</option>
                  <option value='30' selected={(data.time_interval_val === 30)}>Last 30 minutes</option>
                  <option value='60' selected={(data.time_interval_val === 60)}>Last 1 hour</option>
                  <option value='360' selected={(data.time_interval_val === 360)}>Last 6 hours</option>
                  <option value='720' selected={(data.time_interval_val === 720)}>Last 12 hours</option>
                  <option value='1440' selected={(data.time_interval_val === 1440)}>Last 24 hours</option>
                </Input>
              </FormGroup>
            </Col>
            <Col sm='12'>
              {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'>{t('Submit')}</Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' />&nbsp;{t('Saving')}</Button.Ripple>}</Col>
          </Row>
        </div>
      </Form>
    </Card>
  )
}

export default NotificationsTabContent

