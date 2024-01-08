// ================================================================================================
//  File Name: basicDetails.js
//  Description: Details of the Administration ( Add Organization Location Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
//project libraries
import React, { useState, useEffect } from 'react'
import { Form, Label, Input, FormFeedback, Col, Row, Button } from 'reactstrap'
import Select from 'react-select'
import { ArrowRight } from 'react-feather'
import * as yup from 'yup'
import { useForm, Controller } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import axios from "@axios"
import { isObjEmpty, selectThemeColors, token } from '@utils'

//set default values for validation
const defaultValues = {
    org_id: '',
    email: '',
    phone_number: '',
    city: '',
    country_id: '',
    timezone_id: '',
    address: '',
    gst_id: '',
    gst_image: '',
    tan_id: '',
    tan_image: '',
    pan_id: '',
    pan_image: '',
    cin_id: '',
    cin_image: '',
    fax_number: '',
    state: '',
    pincode: '',
    customer_types: '',
    environment_type: '',
    billing_id: ''
}

const BasicDetails = ({ stepper, locationId, setLocationId }) => {
    const [orgData, setOrgData] = useState([])
    const [countriesData, setCountriesData] = useState([])
    const [timeZoneData, setTimeZoneData] = useState([])
    const [planData, setPlanData] = useState([])
    const [billData, setBillData] = useState([])
    const [isLoading, setIsLoading] = useState(false)


    //Get all data from DB by API.
    useEffect(() => {
        axios.get(`/add-location-get-org`, { headers: { Authorization: token() } })
            .then(res => {
                if (res.data.message_type === "data_found") {
                    const orgList = []
                    if (res.data.data.length > 0) {
                        res.data.data.forEach((element, index) => {
                            orgList[index] = { value: element.organization_id, label: `${element.organization_name}` }
                        })
                    }
                    setOrgData(orgList)
                }
            })

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

        axios.get(`/planlist/`, { headers: { Authorization: token() } }).then(res => {
            if (res.data.message_type === "data_found") {
                const planList = []
                if (res.data.data.length > 0) {
                    res.data.data.forEach((element, index) => {
                        planList[index] = { value: element.id, label: element.plan_name }
                    })
                }
                setPlanData(planList)
            }
        })

        axios.get(`/billinglist/`, { headers: { Authorization: token() } }).then(res => {
            if (res.data.message_type === "data_found") {
                const billList = []
                if (res.data.data.length > 0) {
                    res.data.data.forEach((element, index) => {
                        billList[index] = { value: element.id, label: element.billing_types }
                    })
                }
                setBillData(billList)
            }
        })

    }, [])

    function isObjEmpty(obj) {
        return Object.keys(obj).length === 0
    }

    //Validation Schema using Yup
    const BasicDetailsSchema = yup.object().shape({
        org_id: yup.string().required('Please select an organization'),
        email: yup.string().email('Invalid email address').required('Please enter your email address'),
        phone_number: yup.string().matches(/^\d+$/, 'Please enter a valid phone number').required('Please enter your phone number'),
        city: yup.string().required('Please enter the city name'),
        country_id: yup.string().required('Please select a country'),
        timezone_id: yup.string().required('Please select a time zone'),
        billing_id: yup.string().required('Please select a Billing'),
        address: yup.string().required('Please enter the full address'),
        gst_id: yup.string().required('Please enter the GST ID'),
        gst_image: yup.string().required('Please upload the GST image'),
        tan_id: yup.string().required('Please enter the TAN ID'),
        tan_image: yup.string().required('Please upload the TAN image'),
        pan_id: yup.string().required('Please enter the PAN ID'),
        pan_image: yup.string().required('Please upload the PAN image'),
        cin_id: yup.string().required('Please enter the CIN ID'),
        cin_image: yup.string().required('Please upload the CIN image'),
        fax_number: yup.string().matches(/^\d+$/, 'Please enter a valid fax number').required('Please enter the fax number'),
        state: yup.string().required('Please enter the state'),
        pincode: yup.string().required('Please enter the pincode'),
        customer_types: yup.string().required('Please select customer types'),
        environment_type: yup.string().required('Please select environment type')
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

            const searchParams = new URLSearchParams(window.location.search)
            const bodyFormData = new FormData(event.target)

            axios("add-location-step-one", {
                method: "post",
                data: bodyFormData,
                headers: { Authorization: token() }
            })
                .then(res => {
                    setIsLoading(false)
                    if (res.data.message_type === 'successfully_inserted') {
                        searchParams.set('location_id', res.data.location_id)
                        const newUrl = `?${searchParams.toString()}`
                        window.history.pushState(null, '', newUrl)
                        stepper.next()
                    }
                })
                .catch(e => {
                    setIsLoading(false)
                    console.log(e.message)
                })
        }
    }

    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <Row>
                <Col md='6' className='mb-1'>
                    <Label for="org_id">The Name Of Organization</Label>
                    <Controller
                        id='org_id'
                        name="org_id"
                        control={control}
                        render={({ field: { onChange, value } }) => (<Select
                            name="org_id"
                            isClearable={true}
                            className='react-select'
                            classNamePrefix='select'
                            options={orgData}
                            theme={selectThemeColors}
                            value={orgData.find((c) => c.value === value)}
                            onChange={(val) => onChange(val.value)}
                        />)}
                    />
                    {errors.org_id ? <div className="invalid-feedback d-block">{errors.org_id.message}</div> : null}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="email">
                        Email ID
                    </Label>
                    <Controller
                        id='email'
                        name="email"
                        control={control}
                        render={({ field }) => <Input type='email' placeholder='Email Id' invalid={errors.email && true} {...field} />}
                    />

                    {errors.email && <FormFeedback>{errors.email.message}</FormFeedback>}

                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="phone_number">
                        Phone Number
                    </Label>
                    <Controller
                        id='phone_number'
                        name="phone_number"
                        control={control}
                        render={({ field }) => <Input type='number' placeholder='Phone Number' invalid={errors.phone_number && true} {...field} />}
                    />
                    {errors.phone_number && <FormFeedback>{errors.phone_number.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="city">
                        City
                    </Label>
                    <Controller
                        id='city'
                        name="city"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder="City" invalid={errors.city && true} {...field} />}
                    />
                    {errors.city && <FormFeedback>{errors.city.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="state">
                        State
                    </Label>
                    <Controller
                        id='state'
                        name="state"
                        control={control}
                        render={({ field }) => <Input type='text' name="state" placeholder="state" invalid={errors.state && true} {...field} />}
                    />
                    {errors.state && <FormFeedback>{errors.state.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label'>Time Zone</Label>
                    <Controller
                        id='timezone_id'
                        name="timezone_id"
                        control={control}
                        render={({ field: { onChange, value } }) => (<Select
                            name="timezone_id"
                            isClearable={true}
                            className='react-select'
                            classNamePrefix='select'
                            options={timeZoneData}
                            theme={selectThemeColors}
                            value={timeZoneData.find((c) => c.value === value) || null} // Set default value as null
                            onChange={(val) => onChange(val?.value || null)} // Use optional chaining and nullish coalescing operator to handle undefined or null values
                        />)}
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
                    <Label className='form-label' for="pincode">
                        Pincode
                    </Label>
                    <Controller
                        id='pincode'
                        name="pincode"
                        control={control}
                        render={({ field }) => <Input type='text' name="pincode" placeholder="pincode" invalid={errors.pincode && true} {...field} />}
                    />
                    {errors.pincode && <FormFeedback>{errors.pincode.message}</FormFeedback>}
                </Col>
            </Row>
            <Row>
                <Col md='12' className='mb-1'>
                    <Label className='form-label'>
                        Full Address
                    </Label>
                    <Controller
                        id='address'
                        name="address"
                        control={control}
                        render={({ field }) => <Input type='textarea' placeholder='Full Address' invalid={errors.address && true} {...field} />}
                    />
                    {errors.address && <FormFeedback>{errors.address.message}</FormFeedback>}
                </Col>
            </Row>
            <div className='content-header col-12 mt-2'>
                <h5 className='mb-0'>Billing Details</h5>
                <small className='text-muted'>Add  Your Billing Details.</small>
                <hr />
            </div>

            <Row>
                <Col md='6' className='mb-1'>
                    <Label className='form-label'>
                        Billing  Type
                    </Label>
                    <Controller
                        id='billing_id'
                        name="billing_id"
                        control={control}
                        render={({ field: { onChange, value } }) => (<Select
                            name="billing_id"
                            isClearable={true}
                            className='react-select'
                            classNamePrefix='select'
                            options={billData}
                            theme={selectThemeColors}
                            value={billData.find((c) => c.value === value) || null} // Set default value as null
                            onChange={(val) => onChange(val?.value || null)} // Use optional chaining and nullish coalescing operator to handle undefined or null values
                        />)}
                    />
                    {errors.billing_id ? <div className="invalid-feedback d-block">{errors.billing_id.message}</div> : null}
                </Col>
            </Row>
            <div className='content-header col-12 mt-2'>
                <h5 className='mb-0'>GST Details</h5>
                <small className='text-muted'>Add  Your GST Details.</small>
                <hr />
            </div>
            <Row>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="gst_id">
                        GST ID
                    </Label>
                    <Controller
                        id='gst_id'
                        name="gst_id"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='GST ID' invalid={errors.gst_id && true} {...field} />}
                    />
                    {errors.gst_id && <FormFeedback>{errors.gst_id.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="gst_image">
                        GST Photo
                    </Label>
                    <Controller
                        id='gst_image'
                        name="gst_image"
                        control={control}
                        render={({ field }) => <Input type='file' invalid={errors.gst_image && true} {...field} accept="image/ " />}
                    />
                    {errors.gst_image && <FormFeedback>{errors.gst_image.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="tan_id">
                        TAN ID
                    </Label>
                    <Controller
                        id='tan_id'
                        name="tan_id"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='TAN ID' invalid={errors.tan_id && true} {...field} />}
                    />
                    {errors.tan_id && <FormFeedback>{errors.tan_id.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="tan_image">
                        TAN Photo
                    </Label>
                    <Controller
                        id='tan_image'
                        name="tan_image"
                        control={control}
                        render={({ field }) => <Input type='file' invalid={errors.tan_image && true} {...field} accept="image/ " />}
                    />
                    {errors.tan_image && <FormFeedback>{errors.tan_image.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="pan_id">
                        PAN Number
                    </Label>
                    <Controller
                        id='pan_id'
                        name="pan_id"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='PAN Number' invalid={errors.pan_id && true} {...field} />}
                    />
                    {errors.pan_id && <FormFeedback>{errors.pan_id.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="pan_image">
                        PAN Photo
                    </Label>
                    <Controller
                        id='pan_image'
                        name="pan_image"
                        control={control}
                        render={({ field }) => <Input type='file' invalid={errors.pan_image && true} {...field} accept="image/ " />}
                    />
                    {errors.pan_image && <FormFeedback>{errors.pan_image.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="cin_id">
                        CID ID
                    </Label>
                    <Controller
                        id='cin_id'
                        name="cin_id"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='CID ID' invalid={errors.cin_id && true} {...field} />}
                    />
                    {errors.cin_id && <FormFeedback>{errors.cin_id.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="cin_image">
                        CID Photo
                    </Label>
                    <Controller
                        id='cin_image'
                        name="cin_image"
                        control={control}
                        render={({ field }) => <Input type='file' invalid={errors.cin_image && true} {...field} accept="image/ " />}
                    />
                    {errors.cin_image && <FormFeedback>{errors.cin_image.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="fax_number">
                        Fax Number
                    </Label>
                    <Controller
                        id='fax_number'
                        name="fax_number"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='Fax Number' invalid={errors.fax_number && true} {...field} />}
                    />
                    {errors.fax_number && <FormFeedback>{errors.fax_number.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="customer_types">
                        Customer Types
                    </Label>
                    <Controller
                        id='customer_types'
                        name="customer_types"
                        control={control}
                        render={({ field }) => <Input type='select' invalid={errors.customer_types && true} {...field}>
                            <option value='' disabled selected>...Select...</option>
                            <option value='1'>New</option>
                            <option value='2'>Returning</option>
                            <option value='3'>Referrals</option>
                        </Input>}
                    />
                    {errors.customer_types && <FormFeedback>{errors.customer_types.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="environment_type">
                        Environment Type
                    </Label>
                    <Controller
                        id='environment_type'
                        name="environment_type"
                        control={control}
                        render={({ field }) => <Input type='select' invalid={errors.environment_type && true} {...field}>
                            <option value='' disabled selected>...Select...</option>
                            <option value='1'>Self Manage</option>
                            <option value='2'>Admin Manage</option>
                        </Input>}
                    />
                    {errors.environment_type && <FormFeedback>{errors.environment_type.message}</FormFeedback>}
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
                            Next <ArrowRight size={14} className="ml-25" />
                        </>
                    )}
                </Button.Ripple>
            </div>
        </Form>
    )
}

export default BasicDetails