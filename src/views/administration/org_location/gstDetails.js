// ================================================================================================
//  File Name: gstDetails.js
//  Description: Details of the Administration ( Add Organization Location Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
//project libraries
import React, { Fragment, useState, useEffect } from 'react'
import { Form, Label, Input, FormFeedback, Col, Row, Button } from 'reactstrap'
import { ArrowLeft, ArrowRight } from 'react-feather'
import * as yup from 'yup'
import { useForm, Controller } from 'react-hook-form'

//customized library
import { yupResolver } from '@hookform/resolvers/yup'
import { isObjEmpty } from '@utils'
import axios from "@axios"

//set default values for validation
const defaultValues = {
    gst_id: '',
    gst_image: '',
    tan_id: '',
    tan_image: '',
    pan_id: '',
    pan_image: '',
    cin_id: '',
    cin_image: '',
    fax_number: ''
}

const GSTDetails = ({ stepper, locationId }) => {

    //check validation schema using Yup library.
    const BasicDetailsSchema = yup.object().shape({
        gst_id: yup.string().required(),
        gst_image: yup.string().required(),
        tan_id: yup.string().required(),
        tan_image: yup.string().required(),
        pan_id: yup.string().required(),
        pan_image: yup.string().required(),
        cin_id: yup.string().required(),
        cin_image: yup.string().required(),
        fax_number: yup.string()
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
            const formData = new FormData(event.target)
            
            axios(`/add-location-step-two?location_id=${locationId}`,{
                method: "post",
                data: formData
            })
            .then(res => {
                if (res.data.message_type == "success") {
                    stepper.next()
                }                
            })
            .catch(e => {
                console.log(e.message)
            })
            
        }
    }

    console.log({locationId})

    return (
        <Form onSubmit={handleSubmit(onSubmit)} >
            <Row>
                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="gst_id">
                        GST ID *
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
                        GST Photo *
                    </Label>
                    <Controller
                        id='gst_image'
                        name="gst_image"
                        control={control}
                        render={({ field }) => <Input type='file' invalid={errors.gst_image && true} {...field} accept="image/*" />}
                    />
                    {errors.gst_image && <FormFeedback>{errors.gst_image.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="tan_id">
                        TAN ID *
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
                        TAN Photo *
                    </Label>
                    <Controller
                        id='tan_image'
                        name="tan_image"
                        control={control}
                        render={({ field }) => <Input type='file' invalid={errors.tan_image && true} {...field} accept="image/*" />}
                    />
                    {errors.tan_image && <FormFeedback>{errors.tan_image.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="pan_id">
                        PAN Number *
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
                        PAN Photo *
                    </Label>
                    <Controller
                        id='pan_image'
                        name="pan_image"
                        control={control}
                        render={({ field }) => <Input type='file' invalid={errors.pan_image && true} {...field} accept="image/*" />}
                    />
                    {errors.pan_image && <FormFeedback>{errors.pan_image.message}</FormFeedback>}
                </Col>

                <Col md='6' className='mb-1'>
                    <Label className='form-label' for="cin_id">
                        CID ID *
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
                        CID Photo *
                    </Label>
                    <Controller
                        id='cin_image'
                        name="cin_image"
                        control={control}
                        render={({ field }) => <Input type='file' invalid={errors.cin_image && true} {...field} accept="image/*" />}
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

            </Row>

            <div className='d-flex justify-content-between mt-2'>
                <Button type='button' color='primary' className='btn-prev' onClick={() => stepper.previous()}>
                    <ArrowLeft size={14} className='align-middle me-sm-25 me-0'></ArrowLeft>
                    <span className='align-middle d-sm-inline-block d-none'>Previous</span>
                </Button>
                <Button type='submit' color='primary' className='btn-next'>
                    <span className='align-middle d-sm-inline-block d-none'>Next</span>
                    <ArrowRight size={14} className='align-middle ms-sm-25 ms-0'></ArrowRight>
                </Button>
            </div>
        </Form >
    )
}

export default GSTDetails