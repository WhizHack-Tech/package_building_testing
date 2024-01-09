// ================================================================================================
//  File Name: filterTypes.js
//  Description: Details of the Administration ( Add Organization Location Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
//project libraries
import React, { useState, useEffect, useReducer } from 'react'
import { Form, Label, Col, Row, Button } from 'reactstrap'
import { ArrowLeft, X, Plus } from 'react-feather'
import Select from 'react-select'

//customized library
import { selectThemeColors } from "@utils"
import Repeater from '@components/repeater'
import axios from "@axios"

const globleState = {
    loading: true,
    data: [],
    optionData: [],
    selectedVals: [],
    // selectedData: { select_0: { type_id: null, values_id: null } }
}

const reducer = (state, action) => {
    switch (action.type) {
        case "FETCH_SUCCESS":
            return {
                ...state,
                loading: false,
                data: action.payload
            }
        case "OPTION_DATA":
            return {
                ...state,
                optionData:action.payload
            }
        case "SET_SELECTED_VALUES":
            return {
                ...state,
                selectedVals: { ...state.selectedVals, ...action.payload }
            }
        case "ADD":
            return {
                ...state,
                data: { ...state.data, ...action.payload }
            }
        case "DELETE":
            delete state.data[action.payload]
            return {
                ...state
            }
    }
}

const FilterType = ({ stepper }) => {
    const [state, dispatch] = useReducer(reducer, globleState)
    const [repeateOneCount, setRepeateOneCount] = useState(1)
    const [filterOption, setFilterOption] = useState([])
    const [databaseData, setDatabaseData] = useState([])

    const increaseCount = () => {
        setRepeateOneCount(repeateOneCount + 1)
        dispatch({
            type: "ADD",
            payload: { [`product_${repeateOneCount}`]: { product_id: null, db_id: null } }
        })
    }

    const deleteForm = e => {
        e.preventDefault()
        e.target.closest('div.parent-box').remove()
        let dataID = e.target.closest('div.parent-box').getAttribute("dataid")
        dispatch({
            type: "DELETE",
            payload: `product_${dataID}`
        })
    }
    useEffect(() => {
        axios.get(`/get-filter-details`)
            .then(res => {
                if (res.data.message_type === "data_found") {

                    const filterListData = []
                    if (res.data.data.length > 0) {
                        res.data.data.forEach((element, index) => {
                            filterListData[index] = { value: element.name_alias, label: `${element.name}` }
                        });
                    }

                    dispatch({
                        type: "OPTION_DATA",
                        payload: filterListData
                    })

                    dispatch({
                        type: "FETCH_SUCCESS",
                        payload: res.data.data
                    })                    
                }
            })
            .catch(error => {
                console.log(error.message);
            });
    }, [])

    useEffect(() => {
        console.log(state)
    },[state])
    

    const formSubmit = (event) => {
        event.preventDefault()
        const updateProductObject = []
        if (Object.keys(state.data).length > 0) {
            for (const key in state.data) {
                updateProductObject.push(state.data[key])
            }
        }
        console.log(updateProductObject)
    }

    return (<Form onSubmit={formSubmit}>

        <Repeater count={repeateOneCount}>
            {
                repeateOne => (
                    <div key={`parent_box_${repeateOne}`} dataid={repeateOne} className='border border-primary parent-box rounded p-2 mb-2'>
                        <Row className='justify-content-between align-items-end'>
                            <Col md='6' className='mb-1'>
                                <Label>Filter Type *</Label>
                                <Select
                                    isClearable={false}
                                    className='react-select'
                                    classNamePrefix='select'
                                    theme={selectThemeColors}
                                    options={state.optionData}
                                />
                            </Col>

                            <Col md='6' className='mb-1'>
                                <Label>Filter Values *</Label>
                                <Select
                                    isClearable={false}
                                    className='react-select'
                                    classNamePrefix='select'
                                />
                            </Col>
                            <Col md={2}>
                                <Button color='danger' className='text-nowrap px-1 my-1' onClick={deleteForm} outline>
                                    <X size={14} className='me-50' />
                                    <span>Delete</span>
                                </Button>
                            </Col>
                        </Row>
                    </div>
                )
            }
        </Repeater>
        <Button className='btn-icon' color='primary' onClick={increaseCount}>
            <Plus size={14} />
            <span className='align-middle ms-25'>Add New</span>
        </Button>
        <hr />


        <div className='d-flex justify-content-between mt-2'>
            <Button type='button' color='primary' className='btn-prev' onClick={() => stepper.previous()}>
                <ArrowLeft size={14} className='align-middle me-sm-25 me-0'></ArrowLeft>
                <span className='align-middle d-sm-inline-block d-none'>Previous</span>
            </Button>
            <Button type='submit' color='primary' className='btn-next'>
                <span className='align-middle d-sm-inline-block d-none'>Submit</span>
            </Button>
        </div>
    </Form>)
}

export default FilterType