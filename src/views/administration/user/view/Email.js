// ================================================================================================
//  File Name: Email.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import { useState, useEffect, Fragment } from 'react'
import {
  Button,
  Label,
  FormGroup,
  Col,
  Row,
  Spinner,
  Form
} from 'reactstrap'
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../../constants/api_message'
import { FormattedMessage } from 'react-intl'
import Select from 'react-select'
import { useParams } from 'react-router-dom'
import "./Loader.css"
const MySwal = withReactContent(Swal)

const EmailTabContent = () => {
  const [btnLoader, setBtnLoader] = useState(false)
  const [pageLoad, setPageLoad] = useState(false)
  const [platformVal, setPlatformVal] = useState([])
  const [emailsVal, setEmailsVal] = useState([])
  const [email, setEmail] = useState([])

  const { id, activated_plan_id } = useParams()

  const platform = [
    { value: 'aws', label: 'Aws', color: '#00B8D9', isFixed: true },
    { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
    { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
  ]

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

    const getConfig = await axios.get(`/all-config?config_type=email_config_live&location_id=${id}&activated_plan_id=${activated_plan_id}`, { headers: { Authorization: token() } })

    if (getConfig.data.message_type === 'data_found') {
      const DATA = getConfig.data.data
    
      if (DATA && DATA.length > 0) {
        const firstConfig = DATA[0]
        setPlatformVal(findValOption(firstConfig.platform_val, platform))
    
        if (getEmails.data.message_type === "d_found") {
          const mail_ids = getEmails.data.data.map((item) => ({
            value: item.email,
            label: item.email,
            color: '#00B8D9'
          }))
          setEmail(mail_ids)
          setEmailsVal(findValOption(firstConfig.email_ids, mail_ids))
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
    bodyFormData.append('location_id', id)
    bodyFormData.append('activated_plan_id', activated_plan_id)

    axios({
      method: 'post',
      url: '/add-email-config-update',
      data: bodyFormData,
      headers: { Authorization: token() }
    })
      .then((res) => {
        setBtnLoader(false)
        if (res.data.message_type === 'updated successfully') {
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
              <Label>
                <FormattedMessage id='Email' />
              </Label>
              <Select
                id="email_ids"
                isClearable={false}
                theme={selectThemeColors}
                isMulti
                name='email_ids[]'
                options={email}
                defaultValue={emailsVal}
                className='react-select'
                classNamePrefix='select'
              />
            </FormGroup>
          </Col>
          <Col className='mb-1' md='6' sm='12'>
            <Label>
              <FormattedMessage id='Platform' />
            </Label>
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
          <Col className='mt-1 d-flex justify-content-end' sm='12'>
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
    </Fragment>
  )
}

export default EmailTabContent
