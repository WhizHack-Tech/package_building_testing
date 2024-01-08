// ================================================================================================
//  File Name: groupMailConfig.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import React, { useState, useEffect, Fragment } from 'react'
import {
  Button,
  Label,
  FormGroup,
  Col,
  Row,
  Spinner,
  Form,
  Badge,
  Input
} from 'reactstrap'
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../../constants/api_message'
import { FormattedMessage } from 'react-intl'
import Select from 'react-select'
import { useParams } from 'react-router-dom'
import { X } from 'react-feather'
import "./Loader.css"
import './multiple-tabs.css'
const MySwal = withReactContent(Swal)


function TagsInput({ setTagLists, tagLists }) {
  const [tags, setTags] = useState(tagLists.length > 0 ? tagLists : [])

  useEffect(() => {
    setTagLists(tags)
  }, [tags])

  function handleKeyDown(e) {

    if (e.key !== ',' && e.key !== 'Enter' && e.key !== ' ') return
    const value = e.target.value
    if (!value.trim()) return
    setTags([...tags, value.split(",").join("").trim()])
    e.target.value = null
  }

  function removeTag(index) {
    setTags(tags.filter((el, i) => i !== index))
  }

  return (
    <React.Fragment>
      <Label className='form-label'>Master Emails</Label>
      <div className="tags-input-container">
        {tags.map((tag, index) => (
          <Badge key={index} color='primary'>
            <span className='align-middle pr-1'>{tag}</span>
            <X size={12} className='align-middle cursor' onClick={() => removeTag(index)} />
          </Badge>
        ))}
        <Input onKeyDown={handleKeyDown} type="text" className="tags-input" placeholder="Emails" />
      </div>
    </React.Fragment>
  )
}

const GroupMailConfig = () => {
  const [btnLoader, setBtnLoader] = useState(false)
  const [pageLoad, setPageLoad] = useState(false)
  const [emailsVal, setEmailsVal] = useState([])
  const [email, setEmail] = useState([])
  const [tagLists, setTagLists] = useState([])

  const { id, activated_plan_id } = useParams()

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

  const apiCalls = async () => {
    setPageLoad(true)

    const getEmails = await axios.get(`/email-display?location_id=${id}&activated_plan_id=${activated_plan_id}`, { headers: { Authorization: token() } })

    const getConfig = await axios.get(`/display-hc-sensor-alert-email?config_type=email_config_live&location_id=${id}&activated_plan_id=${activated_plan_id}`, { headers: { Authorization: token() } })
    if (getConfig.data.message_type === 'data_found') {
      const DATA = getConfig.data.data

      if (DATA[0].sensor_alert_admin !== undefined && DATA[0].sensor_alert_admin !== null) {

        if (DATA[0].sensor_alert_admin.trim().length > 3) {
          const adminEmails = (DATA[0].sensor_alert_admin).split(",")
          setTagLists(adminEmails)
        }

      }

      if (getEmails.data.message_type === "d_found") {

        const mail_ids = getEmails.data.data.map((item) => ({
          value: item.email,
          label: item.email,
          color: '#00B8D9'
        }))

        setEmail(mail_ids)
        if (DATA[0].sensor_alert_client !== undefined && DATA[0].sensor_alert_client !== null) {
          setEmailsVal(findValOption(DATA[0].sensor_alert_client, mail_ids))
        }
      }

    }

    setPageLoad(false)

  }

  useEffect(() => {
    apiCalls()
  }, [])


  function submitForm(event) {
    setBtnLoader(true)
    event.preventDefault()

    const bodyFormData = new FormData(event.target)
    bodyFormData.append('config_type', 'email_config_live')
    bodyFormData.append('admin_emails', tagLists)
    bodyFormData.append('location_id', id)
    bodyFormData.append('activated_plan_id', activated_plan_id)

    axios({
      method: 'post',
      url: '/add-hc-sensor-alert-email',
      data: bodyFormData,
      headers: { Authorization: token() }
    })
      .then((res) => {
        setBtnLoader(false)
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
        <div className="tri-color-ripple-spinner">
          <div className="ripple ripple1"></div>
          <div className="ripple ripple2"></div>
        </div>
      </div>
    )
  }

  return (
    <Fragment>
      <Form onSubmit={submitForm}>
        <Row>
          <Col sm='6'>
            <FormGroup>
              <Label>Client Email</Label>
              <Select
                id="client_emails"
                isClearable={false}
                theme={selectThemeColors}
                isMulti
                name='client_emails[]'
                options={email}
                defaultValue={emailsVal}
                className='react-select'
                classNamePrefix='select'
              />
            </FormGroup>
          </Col>
          <Col sm="6">
            <TagsInput setTagLists={setTagLists} tagLists={tagLists} />
          </Col>

          <Col className='mt-1 d-flex justify-content-end' sm='12'>
            {btnLoader === false ? (
              <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'>
                <FormattedMessage id='Submit' onSubmit={(event) => event.preventDefault()} />
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
    </Fragment>
  )
}

export default GroupMailConfig
