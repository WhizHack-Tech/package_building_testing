// ================================================================================================
//  File Name: NotificatinTabContent.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect } from 'react'
import { Row, Col, CustomInput, CardHeader, Input } from 'reactstrap'
import axios from "@axios"
import { token } from '@utils'
import { toast } from 'react-toastify'
import { useTranslation } from 'react-i18next'

// Tooogle button function
const NotificationsTabContent = ({ data }) => {
  const {t} = useTranslation()
  const [mfa, setMfa] = useState(false)
  const [email, setEmail] = useState(false)
  const [notification, setNotification] = useState(false)
  // email switch //
  const setEmailnote = (event) => {
    setEmail(event.target.checked)
    let emailCheck = false
    if (event.target.checked) {
      emailCheck = true
    } else {
      emailCheck = false
    }

    axios.post('/active-init-config', {
      is_active: emailCheck,
      config_type: "email_config_live"
    }, { headers: { Authorization: token() } }).then(res => {

      if (res.data.message_type === "is_active_update") {
        let emailCheckDb = false
        let emailCheckActive = "deactive"
        if (res.data.data === true) {
          emailCheckDb = true
          emailCheckActive = "actived"
        } else {
          emailCheckDb = false
          emailCheckActive = "deactived"
        }

        toast.success(`Email notification is ${emailCheckActive}`, {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined
        })
        setEmail(emailCheckDb)
      }
    })
  }
  // MFA switch //
  const setMfaFun = (event) => {
    setMfa(event.target.checked)
    let mfaCheck = 0
    if (event.target.checked) {
      mfaCheck = 1
    } else {
      mfaCheck = 0
    }

    axios.post('/account-maf', {
      allow_MFA: mfaCheck
    }, { headers: { Authorization: token() } }).then(res => {

      if (res.data.message_type === "allow_mfa_update") {
        let mfaCheckDb = 0
        let mfaCheckActive = "Deactive"
        if (res.data.data === 1) {
          mfaCheckDb = 1
          mfaCheckActive = "Active"
        } else {
          mfaCheckDb = 0
          mfaCheckActive = "Deactive"
        }

        toast.success(`MFA | Multifactor Authentication is ${mfaCheckActive}`, {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined
        })
        setMfa(mfaCheckDb)
      }
    })

  }

  useEffect(() => {
    if (data.allow_MFA === 1) {
      setMfa(true)
    } else {
      setMfa(false)
    }

    axios.get('/display-config?config_type=email_config_live', { headers: { Authorization: token() } }).then(
      res => {
        if (res.data.message_type === "data_found") {
          setEmail(res.data.data[0].is_active)
        }
      }
    )

    axios.get('/display-config?config_type=notification_live', { headers: { Authorization: token() } }).then(
      res => {
        if (res.data.message_type === "data_found") {
          setNotification(res.data.data[0].is_active)
        }
      }
    )
  }, [])
  // Notification Switch
  const setNotificationnote = (event2) => {
    setNotification(event2.target.checked)
    let notificationCheck = false
    if (event2.target.checked) {
      notificationCheck = true
    } else {
      notificationCheck = false
    }

    axios.post('/active-init-config', {
      is_active: notificationCheck,
      config_type: "notification_live"
    }, { headers: { Authorization: token() } }).then(res => {

      if (res.data.message_type === "is_active_update") {
        let notificationCheckDb = false
        let notificationCheckActive = "deactive"
        if (res.data.data === true) {
          notificationCheckDb = true
          notificationCheckActive = "actived"
        } else {
          notificationCheckDb = false
          notificationCheckActive = "deactived"
        }

        toast.success(`Dashboard notification is ${notificationCheckActive}`, {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined
        })
        setNotification(notificationCheckDb)
      }
    })
  }


  return (
    <Row>
      {/* <CardHeader>
        <CardTitle tag='h4'>Activity</CardTitle>
      </CardHeader> */}
      <div style={{ height: '140px' }}>
        <h6 className='section-label mx-1 mb-2'>{t('Notification')}</h6>
        <Col sm='12' className='mb-2'>
          <CustomInput
            type='switch'
            id='mfa_check'
            checked={mfa}
            onChange={setMfaFun}
            label={t('MFA | Multifactor Authentication')}
          />
        </Col>
        <Col sm='12' className='mb-2'>
          <CustomInput
            type='switch'
            id='is_active'
            checked={email}
            onChange={setEmailnote}
            label={t('Email Notifications')}
            defaultChecked
          />
        </Col>
        <Col sm='12' className='mb-2'>
          <CustomInput
            type='switch'
            id='is_active2'
            checked={notification}
            onChange={setNotificationnote}
            label={t('Dashboard Notifications')}
            defaultChecked
          />
        </Col>
      </div>
    </Row>
  )
}

export default NotificationsTabContent
