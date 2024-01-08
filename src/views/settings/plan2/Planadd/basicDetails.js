// ================================================================================================
//  File Name: basicDetails.js
//  Description: Details of the Setting ( Plan Add ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
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
import "flatpickr/dist/flatpickr.css"
import "flatpickr/dist/themes/dark.css"
import Flatpickr from 'react-flatpickr'

//set default values for validation
const defaultValues = {
    plan_name: '',
    plan_descriptions: ''

}

const BasicDetails = ({ stepper }) => {
    const [isLoading, setIsLoading] = useState(false)
    const [startDate, setStartDate] = useState(new Date())
    const [endDate, setEndDate] = useState(new Date())


    function isObjEmpty(obj) {
        return Object.keys(obj).length === 0
    }

    //Validation Schema using Yup
    const BasicDetailsSchema = yup.object().shape({
        plan_name: yup.string().required('Please enter Plan Name'),
        plan_descriptions: yup.string().required('Please enter Plan Descriptions')

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

            axios("add-plan-step-one", {
                method: "post",
                data: bodyFormData,
                headers: { Authorization: token() }
            })
                .then(res => {
                    setIsLoading(false)
                    if (res.data.message_type === 'successfully_inserted') {
                        searchParams.set('plan_id', res.data.plan_id)
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
                    <Label className='form-label' for="plan_name">
                        Plan Name
                    </Label>
                    <Controller
                        id='plan_name'
                        name="plan_name"
                        control={control}
                        render={({ field }) => <Input type='text' placeholder='Plan Name' invalid={errors.plan_name && true} {...field} />}
                    />
                    {errors.plan_name && <FormFeedback>{errors.plan_name.message}</FormFeedback>}
                </Col>
                <Col sm='6' className='mb-1'>
                    <Label>Start Date</Label>
                    <Flatpickr
                        className='form-control'
                        name='plan_start_date'
                        value={startDate}
                        onChange={(date) => setStartDate(date[0])}
                        options={{
                            dateFormat: 'Y-m-d',
                            minDate: 'today' // Set the date format to DD-MM-YY
                        }}
                    />
                </Col>
                <Col sm='6' className='mb-1'>
                    <Label>End Date</Label>
                    <Flatpickr
                        className='form-control'
                        name="plan_end_date"
                        value={endDate}
                        onChange={(date) => setEndDate(date[0])}
                        options={{
                            dateFormat: 'Y-m-d',
                            minDate: 'today' // Set the date format to DD-MM-YY
                        }}
                    />
                </Col>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="plan_descriptions">
                        Plan Descriptions
                    </Label>
                    <Controller
                        id='plan_descriptions'
                        name="plan_descriptions"
                        control={control}
                        render={({ field }) => <Input type='textarea' rows="1" placeholder="plan_descriptions" invalid={errors.plan_descriptions && true} {...field} />}
                    />
                    {errors.plan_descriptions && <FormFeedback>{errors.plan_descriptions.message}</FormFeedback>}
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