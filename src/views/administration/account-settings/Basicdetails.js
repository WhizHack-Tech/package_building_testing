// ================================================================================================
//  File Name: Basicdetails.js
//  Description: Details of the Administration ( Add Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
//project libraries
import React, { useState, useEffect } from 'react'
import { useHistory } from 'react-router-dom'
import { Form, Label, Input, FormFeedback, Col, Row, Button } from 'reactstrap'
import Select from 'react-select'
import * as yup from 'yup'
import { useForm, Controller } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import axios from "@axios"
import { selectThemeColors, token } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../constants/api_message"
const MySwal = withReactContent(Swal)
//set default values for validation
const defaultValues = {
  organization_name: '', // Assign a default value here
  organization_primary_email_id: '',
  organization_secondary_email_id: '',
  organization_primary_contact_number: '',
  organization_secondary_contact_number: '',
  organization_address: '',
  organization_city: '',
  organization_state: '',
  organization_pincode: '',
  timezone_id: '',
  country_id: ''
}

const BasicDetails = () => {
  const history = useHistory()
  const [countriesData, setCountriesData] = useState([])
  const [timeZoneData, setTimeZoneData] = useState([])
  const [isLoading, setIsLoading] = useState(false)


  //Get all data from DB by API.
  useEffect(() => {


    axios.get(`/countrydata/`, { headers: { Authorization: token() } }).then(res => {
      if (res.data.message_type === "data_found") {
        const countriesList = []
        if (res.data.data.length > 0) {
          res.data.data.forEach((element, index) => {
            countriesList[index] = { value: element.id, label: `${element.country_name} (${element.country_code})` }
          })
        }
        setCountriesData(countriesList)
      }
    })

    axios.get(`/timezonedata/`, { headers: { Authorization: token() } }).then(res => {
      const timeZoneObj = []
      if (res.data.message_type === 'data_found') {
        if (res.data.data.length > 0) {
          res.data.data.forEach((element, index) => {
            timeZoneObj[index] = { value: element.id, label: `${element.Time_Zone} (${element.GMT_Offset})` }
          })
        }
      }
      setTimeZoneData(timeZoneObj)
    })

  }, [])

  function isObjEmpty(obj) {
    return Object.keys(obj).length === 0
  }

  //Validation Schema using Yup
  const BasicDetailsSchema = yup.object().shape({
    organization_name: yup.string().required('Please Enter an organization'),
    organization_primary_email_id: yup.string().email('Invalid email address').required('Please enter your email address'),
    organization_secondary_email_id: yup.string().email('Invalid email address').required('Please enter your email address'),
    organization_primary_contact_number: yup.string().matches(/^\d+$/, 'Please enter a valid phone number').required('Please enter your phone number'),
    organization_secondary_contact_number: yup.string().matches(/^\d+$/, 'Please enter a valid phone number').required('Please enter your phone number'),
    organization_city: yup.string().required('Please enter the city name'),
    country_id: yup.string().required('Please select a country'),
    timezone_id: yup.string().required('Please select a time zone'),
    organization_address: yup.string().required('Please enter the full address'),
    organization_state: yup.string().required('Please enter the state'),
    organization_pincode: yup.string().required('Please enter the pincode')
  })


  const {
    control,
    handleSubmit,
    formState: { errors }
  } = useForm({
    defaultValues,
    resolver: yupResolver(BasicDetailsSchema)
  })

  const onSubmit = (data, event) => {
    event.preventDefault()
    if (isObjEmpty(errors)) {
      setIsLoading(true)

      const bodyFormData = new FormData(event.target)

      axios("/create/", {
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
            }).then((result) => {
              if (result.isConfirmed) {
                history.push('/administration/user/list') // Redirect to another page after success
              }
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
        }).catch((errors) => {
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
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Row>
        <Col md='6' className='mb-1'>
          <Label className='form-label' for="organization_name">
            Organization Full Name
          </Label>
          <Controller
            id='organization_name'
            name="organization_name"
            control={control}
            render={({ field }) => <Input type='text' placeholder='Organization Full Name' invalid={errors.organization_name && true} {...field} />}
          />

          {errors.organization_name && <FormFeedback>{errors.organization_name.message}</FormFeedback>}

        </Col>

        <Col md='6' className='mb-1'>
          <Label className='form-label' for="organization_primary_email_id">
            Organization Primary Email Address
          </Label>
          <Controller
            id='organization_primary_email_id'
            name="organization_primary_email_id"
            control={control}
            render={({ field }) => <Input type='email' placeholder='Organization Primary Email Address' invalid={errors.organization_primary_email_id && true} {...field} />}
          />

          {errors.organization_primary_email_id && <FormFeedback>{errors.organization_primary_email_id.message}</FormFeedback>}

        </Col>
        <Col md='6' className='mb-1'>
          <Label className='form-label' for="organization_secondary_email_id">
            Organization Secondary Email Address
          </Label>
          <Controller
            id='organization_secondary_email_id'
            name="organization_secondary_email_id"
            control={control}
            render={({ field }) => <Input type='email' placeholder='Organization Secondary Email Address' invalid={errors.organization_secondary_email_id && true} {...field} />}
          />

          {errors.organization_secondary_email_id && <FormFeedback>{errors.organization_secondary_email_id.message}</FormFeedback>}

        </Col>
        <Col md='6' className='mb-1'>
          <Label className='form-label' for="organization_primary_contact_number">
            Organization Primary Phone Number
          </Label>
          <Controller
            id='organization_primary_contact_number'
            name="organization_primary_contact_number"
            control={control}
            render={({ field }) => <Input type='number' placeholder='Organization Primary Phone Number' invalid={errors.organization_primary_contact_number && true} {...field} />}
          />
          {errors.organization_primary_contact_number && <FormFeedback>{errors.organization_primary_contact_number.message}</FormFeedback>}
        </Col>
        <Col md='6' className='mb-1'>
          <Label className='form-label' for="organization_secondary_contact_number">
            Organization Secondary Phone Number
          </Label>
          <Controller
            id='organization_secondary_contact_number'
            name="organization_secondary_contact_number"
            control={control}
            render={({ field }) => <Input type='number' placeholder='Organization Secondary Phone Number' invalid={errors.organization_secondary_contact_number && true} {...field} />}
          />
          {errors.organization_secondary_contact_number && <FormFeedback>{errors.organization_secondary_contact_number.message}</FormFeedback>}
        </Col>
      </Row>
      <div className='content-header'>
        <h5 className='mb-0 ml-1'>Address Details</h5>
        <small className='text-muted ml-1'>Enter Your Address Details.</small>
      </div>
      <Row>
        <Col md='6' className='mb-1'>
          <Label className='form-label' for="organization_city">
            City
          </Label>
          <Controller
            id='organization_city'
            name="organization_city"
            control={control}
            render={({ field }) => <Input type='text' placeholder="City" invalid={errors.organization_city && true} {...field} />}
          />
          {errors.organization_city && <FormFeedback>{errors.organization_city.message}</FormFeedback>}
        </Col>
        <Col md='6' className='mb-1'>
          <Label className='form-label' for="organization_state">
            State
          </Label>
          <Controller
            id='organization_state'
            name="organization_state"
            control={control}
            render={({ field }) => <Input type='text' name="organization_state" placeholder="state" invalid={errors.organization_state && true} {...field} />}
          />
          {errors.organization_state && <FormFeedback>{errors.organization_state.message}</FormFeedback>}
        </Col>
        <Col md='6' className='mb-1'>
          <Label className='form-label'>Time Zone</Label>
          <Controller
            id='timezone_id'
            name="timezone_id"
            control={control}
            render={({ field: { onChange, value } }) => (
              <Select
                name="timezone_id"
                isClearable={true}
                className='react-select'
                classNamePrefix='select'
                options={timeZoneData}
                theme={selectThemeColors}
                value={timeZoneData.find((c) => c.value === value) || null} // Set default value as null
                onChange={(val) => onChange(val?.value || null)} // Use optional chaining and nullish coalescing operator to handle undefined or null values
              />
            )}
          />

          {errors.timezone_id ? <div className="invalid-feedback d-block">{errors.timezone_id.message}</div> : null}
        </Col>
        <Col md='6' className='mb-1'>
          <Label for="country_id">Country</Label>
          <Controller
            id='country_id'
            name="country_id"
            control={control}
            render={({ field: { onChange, value } }) => (<Select
              name="country_id"
              isClearable={true}
              className='react-select'
              classNamePrefix='select'
              options={countriesData}
              theme={selectThemeColors}
              value={countriesData.find((c) => c.value === value) || null} // Set default value as null
              onChange={(val) => onChange(val?.value || null)} // Use optional chaining and nullish coalescing operator to handle undefined or null values
            />)}
          />
          {errors.country_id ? <div className="invalid-feedback d-block">{errors.country_id.message}</div> : null}
        </Col>
        <Col md='6' className='mb-1'>
          <Label className='form-label' for="organization_pincode">
            Pincode
          </Label>
          <Controller
            id='organization_pincode'
            name="organization_pincode"
            control={control}
            render={({ field }) => <Input type='text' name="organization_pincode" placeholder="pincode" invalid={errors.organization_pincode && true} {...field} />}
          />
          {errors.organization_pincode && <FormFeedback>{errors.organization_pincode.message}</FormFeedback>}
        </Col>
      </Row>
      <Row>
        <Col md='12' className='mb-1'>
          <Label className='form-label'>
            Full Address
          </Label>
          <Controller
            id='organization_address'
            name="organization_address"
            control={control}
            render={({ field }) => <Input type='textarea' placeholder='Full Address' invalid={errors.organization_address && true} {...field} />}
          />
          {errors.organization_address && <FormFeedback>{errors.organization_address.message}</FormFeedback>}
        </Col>
      </Row>
      <div className='d-flex justify-content-end'>
        <Button.Ripple type="submit" color="primary" disabled={isLoading}>
          {isLoading ? (
            <div className="spinner-border spinner-border-sm" role="status">
              {/* <span className="visually-hidden">Loading...</span> */}
            </div>
          ) : (
            <>
              Submit
            </>
          )}
        </Button.Ripple>
      </div>
    </Form>
  )
}

export default BasicDetails