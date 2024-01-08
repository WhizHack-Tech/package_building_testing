// ================================================================================================
//  File Name: congifDetails.js
//  Description: Details of the Administration ( Add Organization Location Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
//project libraries
import React, { Fragment, useState, useEffect } from 'react'
import { Form, Label, Input, FormFeedback, Col, Row, Button, CustomInput } from 'reactstrap'
import { ArrowLeft, ArrowRight } from 'react-feather'
import * as yup from 'yup'
import { useForm, Controller } from 'react-hook-form'
import Select from 'react-select'
//customized library
import { yupResolver } from '@hookform/resolvers/yup'
import { isObjEmpty, selectThemeColors, token } from '@utils'
import axios from "@axios"

//set default values for validation
const defaultValues = {
    accuracy_val: [],
    severity_val: [],
    platform_val: [],
    trace_val: [],
    email_platform_val: [],
    email_severity_val: [],
    email_accuracy_val: '',
    email_trace_val: [],
    notification_platform_val: [],
    time_interval_val: '',
    notification_accuracy_val: '',
    notification_trace_val: '',
    db_username: '',
    db_password: '',
    db_host: '',
    db_port: ''
}
let locationId = ''
let planId = ''
const serchState = () => {
    const searchParams = new URLSearchParams(window.location.search)
    locationId = searchParams.get('location_id')
    planId = searchParams.get('plan_id')
}

const Config = ({ stepper }) => {
    const [isLoading, setIsLoading] = useState(false)
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

    const email_platform = [
        { value: 'aws', label: 'AWS', color: '#00B8D9', isFixed: true },
        { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
        { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
    ]

    const email_severity = [
        { value: '1', label: 'High', color: '#00B8D9', isFixed: true },
        { value: '2', label: 'Medium', color: '#0052CC', isFixed: true },
        { value: '3', label: 'Low', color: '#5243AA', isFixed: true }
    ]

    const notification_platform = [
        { value: 'aws', label: 'AWS', color: '#00B8D9', isFixed: true },
        { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
        { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
    ]

    const notification_severity = [
        { value: '1', label: 'High', color: '#00B8D9', isFixed: true },
        { value: '2', label: 'Medium', color: '#0052CC', isFixed: true },
        { value: '3', label: 'Low', color: '#5243AA', isFixed: true }
    ]

    //check validation schema using Yup library.
    const BasicDetailsSchema = yup.object().shape({
        accuracy_val: yup.string().required('Accuracy is required'),
        platform_val: yup.string().required('Platform is required'),
        severity_val: yup.string().required('Severity is required'),
        trace_val: yup.string().required('Trace is required'),
        email_platform_val: yup.string().required('Email Platform is required'),
        email_severity_val: yup.string().required('Email Severity is required'),
        email_accuracy_val: yup.string().required('Email Accuracy is required'),
        email_trace_val: yup.string().required('Email Trace is required'),
        notification_platform_val: yup.string().required('Notification Platform is required'),
        notification_severity_val: yup.string().required('Natification Severity is required'),
        time_interval_val: yup.string().required('Time Interval is required'),
        notification_accuracy_val: yup.string().required('Notification Accuracy is required'),
        notification_trace_val: yup.string().required('Notification Trace is required'),
        db_username: yup.string().required('Database username is required'),
        db_password: yup.string().required('Database Password is required'),
        db_host: yup.string().required('Database Host is required'),
        db_port: yup.string().required('Database Port is required')
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
        serchState()
        event.preventDefault()
        setIsLoading(true)
        if (isObjEmpty(errors)) {
            const bodyFormData = new FormData(event.target)
            const searchParams = new URLSearchParams(window.location.search)
            bodyFormData.append("config_type[]", "dashboard_filter")
            bodyFormData.append("config_type[]", "email_config_live")
            bodyFormData.append("config_type[]", "notification_live")
            bodyFormData.append("location_id", locationId)
            bodyFormData.append("plan_id", planId)
            axios("/add-location-step-three", {
                method: "post",
                data: bodyFormData,
                headers: { Authorization: token() }

            })
                .then(res => {
                    setIsLoading(false)

                    if (res.data.message_type === "successfully_inserted") {
                        
                        stepper.next()

                    } else if (res.data.message_type === "unsuccessful") {
                        Swal.fire({
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
                .catch(e => {
                    setIsLoading(false)
                    console.log(e.message)
                })
        }
    }

    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <Row>
                <div className='content-header col-12 mt-2'>
                    <h5 className='mb-0'>Dashboard Config</h5>
                    <small className='text-muted'>Add  Your Dashboard Config.</small>
                    <hr />
                </div>
                <Col md='6' className='mb-1'>
                    <Label for="platform_val">Platform</Label>
                    <Controller
                        name='platform_val[]'
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.platform_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={platform}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />
                    {errors.platform_val ? <div className="invalid-feedback d-block">{errors.platform_val.message}</div> : null}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label for="severity_val">Threat Severity</Label>
                    <Controller
                        name='severity_val[]'
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.severity_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={severity}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />
                    {errors.severity_val ? <div className="invalid-feedback d-block">{errors.severity_val.message}</div> : null}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="accuracy_val">
                        Accuracy
                    </Label>
                    <Controller
                        id='accuracy_val'
                        name="accuracy_val"
                        control={control}
                        render={({ field }) => <Input type='select' invalid={errors.accuracy_val && true} {...field}>
                            <option value='' disabled selected>...Select...</option>
                            <option value='1'>Between 91% to 100%</option>
                            <option value='2'>Between 76% to 90%</option>
                            <option value='3'>Between 65% to 75%</option>
                        </Input>}
                    />

                    {errors.accuracy_val && <FormFeedback>{errors.accuracy_val.message}</FormFeedback>}

                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="trace_val">
                        Trace
                    </Label>
                    <Controller
                        id='trace_val'
                        name="trace_val[]"
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.trace_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={trace}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />

                    {errors.trace_val && <FormFeedback>{errors.trace_val.message}</FormFeedback>}

                </Col>
            </Row>
            <Row>
                <div className='content-header col-12 mt-2'>
                    <h5 className='mb-0'>Email Config</h5>
                    <small className='text-muted'>Add your Email Config.</small>
                    <hr />
                </div>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="email">
                        Select Email
                    </Label>
                    <Input type='email' name='email' placeholder='Email' />
                </Col>
                {/* <Col md='6' className='mb-1'>
                    <Label className='form-label' for="email">
                        Select Email
                    </Label>
                    <Controller
                        id='email'
                        name="email"
                        control={control}
                        render={({ field }) => <Input type='email' placeholder='Email' invalid={errors.email && true} {...field} />}
                    />
                    {errors.email && <FormFeedback>{errors.email.message}</FormFeedback>}
                </Col> */}
                <Col md='6' className='mb-1'>
                    <Label for="email_platform_val">Platform</Label>
                    <Controller
                        id='email_platform_val'
                        name='email_platform_val[]'
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.email_platform_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={email_platform}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />
                    {errors.email_platform_val ? <div className="invalid-feedback d-block">{errors.email_platform_val.message}</div> : null}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label for="email_severity_val">Threat Severity</Label>
                    <Controller
                        id='email_severity_val'
                        name='email_severity_val[]'
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.email_severity_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={email_severity}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />
                    {errors.email_severity_val ? <div className="invalid-feedback d-block">{errors.email_severity_val.message}</div> : null}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="email_accuracy_val">
                        Accuracy
                    </Label>
                    <Controller
                        id='email_accuracy_val'
                        name="email_accuracy_val"
                        control={control}
                        render={({ field }) => <Input type='select' invalid={errors.email_accuracy_val && true} {...field}>
                            <option value='' disabled selected>...Select...</option>
                            <option value='1'>Between 91% to 100%</option>
                            <option value='2'>Between 76% to 90%</option>
                            <option value='3'>Between 65% to 75%</option>
                        </Input>}
                    />

                    {errors.email_accuracy_val && <FormFeedback>{errors.email_accuracy_val.message}</FormFeedback>}

                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="email_trace_val">
                        Trace
                    </Label>
                    <Controller
                        id='email_trace_val'
                        name="email_trace_val[]"
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.email_trace_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={trace}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />

                    {errors.email_trace_val && <FormFeedback>{errors.email_trace_val.message}</FormFeedback>}

                </Col>

            </Row>
            <Row>
                <div className='content-header col-12 mt-2'>
                    <h5 className='mb-0'>Notification Config</h5>
                    <small className='text-muted'>Add your Notification Config.</small>
                    <hr />
                </div>
                <Col md='6' className='mb-1'>
                    <Label for="notification_platform_val">Platform</Label>
                    <Controller
                        id='notification_platform_val'
                        name='notification_platform_val[]'
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.notification_platform_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={notification_platform}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />
                    {errors.notification_platform_val ? <div className="invalid-feedback d-block">{errors.notification_platform_val.message}</div> : null}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label for="notification_severity_val">Threat Severity</Label>
                    <Controller
                        id='notification_severity_val'
                        name='notification_severity_val[]'
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.notification_severity_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={notification_severity}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />
                    {errors.notification_severity_val ? <div className="invalid-feedback d-block">{errors.notification_severity_val.message}</div> : null}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="time_interval_val">
                        Time Interval
                    </Label>
                    <Controller
                        id='time_interval_val'
                        name="time_interval_val"
                        control={control}
                        render={({ field }) => <Input type='select' invalid={errors.time_interval_val && true} {...field}>
                            <option value='' disabled selected>...Select...</option>
                            <option value='1'>Last 1 minutes</option>
                            <option value='5'>Last 5 minutes</option>
                            <option value='15'>Last 15 minutes</option>
                            <option value='30'>Last 30 minutes</option>
                            <option value='60'>Last 1 hour</option>
                            <option value='360'>Last 6 hours</option>
                            <option value='720'>Last 12 hours</option>
                            <option value='1440'>Last 24 hours</option>
                        </Input>}
                    />

                    {errors.time_interval_val && <FormFeedback>{errors.time_interval_val.message}</FormFeedback>}

                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="notification_accuracy_val">
                        Accuracy
                    </Label>
                    <Controller
                        id='notification_accuracy_val'
                        name="notification_accuracy_val"
                        control={control}
                        render={({ field }) => <Input type='select' invalid={errors.notification_accuracy_val && true} {...field}>
                            <option value='' disabled selected>...Select...</option>
                            <option value='1'>Between 91% to 100%</option>
                            <option value='2'>Between 76% to 90%</option>
                            <option value='3'>Between 65% to 75%</option>
                        </Input>}
                    />

                    {errors.notification_accuracy_val && <FormFeedback>{errors.notification_accuracy_val.message}</FormFeedback>}

                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="notification_trace_val">
                        Trace
                    </Label>
                    <Controller
                        id='notification_trace_val'
                        name="notification_trace_val[]"
                        control={control}
                        render={({ field }) => (
                            <Select
                                invalid={errors.notification_trace_val && true}
                                {...field}
                                isClearable={false}
                                theme={selectThemeColors}
                                isMulti
                                options={trace}
                                className='react-select'
                                classNamePrefix='select'
                            />
                        )}
                    />

                    {errors.notification_trace_val && <FormFeedback>{errors.notification_trace_val.message}</FormFeedback>}

                </Col>

            </Row>
            <Row>
                <div className='content-header col-12 mt-2'>
                    <h5 className='mb-0'>Attach Agent</h5>
                    <small className='text-muted'>Add your Email Attach Agent.</small>
                    <hr />
                </div>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="db_username">
                        Database Username
                    </Label>
                    <Controller
                        id='db_username'
                        name="db_username"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='Database Username' invalid={errors.db_username && true} {...field} />}
                    />
                    {errors.db_username && <FormFeedback>{errors.db_username.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="db_password">
                        Database Password
                    </Label>
                    <Controller
                        id='db_password'
                        name="db_password"
                        control={control}
                        render={({ field }) => <Input type='password' placeholder='Database Password' invalid={errors.db_password && true} {...field} />}
                    />
                    {errors.db_password && <FormFeedback>{errors.db_password.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="db_port">
                        Database Port
                    </Label>
                    <Controller
                        id='db_port'
                        name="db_port"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='Database Port' invalid={errors.db_port && true} {...field} />}
                    />
                    {errors.db_port && <FormFeedback>{errors.db_port.message}</FormFeedback>}
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="db_host">
                        Database Host
                    </Label>
                    <Controller
                        id='db_host'
                        name="db_host"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='Database Host' invalid={errors.db_host && true} {...field} />}
                    />
                    {errors.db_host && <FormFeedback>{errors.db_host.message}</FormFeedback>}
                </Col>
            </Row>
            <div className='d-flex justify-content-between mt-2'>
                <Button type='button' color='primary' className='btn-prev' onClick={() => stepper.previous()}>
                    <ArrowLeft size={14} className='align-middle me-sm-25 me-0'></ArrowLeft>
                    <span className='align-middle d-sm-inline-block d-none'>Previous</span>
                </Button>
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

export default Config
