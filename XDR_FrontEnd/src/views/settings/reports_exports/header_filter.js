// ================================================
//  File Name: header_filter.js
//  Description: Fiter Dynamic Report.
//  -----------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================

import { useState, Fragment, useEffect } from 'react'
import PerfectScrollbar from 'react-perfect-scrollbar'
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, Label, FormGroup, Card, CardBody, Badge } from 'reactstrap'
import { X, Plus } from 'react-feather'
import Select from 'react-select'
import CreatableSelect from 'react-select/creatable'
import { filterApi } from "./store/actions"
import { useSelector, useDispatch } from 'react-redux'
import { selectThemeColors } from '@utils'
import PreLoader from './preLoader'
import "./reports.css"

let addCount = 0
const operatorOptions = [
    { value: 'is', label: 'is' },
    { value: 'is_not', label: 'is not' },
    { value: 'is_null', label: 'is null' },
    { value: 'is_not_null', label: 'is not null' }
]

const HeaderFilter = () => {

    const dispatch = useDispatch()
    const store = useSelector(state => state)
    const { loading, availableListRows, defaultIndexName, rowData } = store.reports_exports
    const timeFilter = store.dashboard_chart

    const [formModal, setFormModal] = useState(false)
    const [filterObj, setFilterObj] = useState([])

    useEffect(() => {
        setFilterObj([])
    }, [timeFilter.values, timeFilter.refreshCount, defaultIndexName])

    const [readState, setState] = useState({
        field_disabled: false,
        condition: null,
        column_name: null,
        value: [],
        selectOptionList: []
    })

    const filterApiCall = (rowData) => {
        const searchQuery = {
            query: rowData,
            index_name: defaultIndexName,
            limit: 20,
            time_filter: timeFilter.values || "last_1_hour"
        }

        if (rowData.length >= 0) {
            dispatch(filterApi(searchQuery))
        }
    }

    const handleOperator = (optVal) => {
        setState(pre => ({ ...pre, condition: optVal.value }))
        if ((optVal.value === "is_null") || (optVal.value === "is_not_null")) {
            setState(pre => ({ ...pre, field_disabled: false, value: "" }))
        } else {
            setState(pre => ({ ...pre, field_disabled: true }))
        }
    }

    const handleRemoveFilter = (index) => {
        const oldFilterObj = filterObj
        const newObj = oldFilterObj.filter(oldData => oldData.filter_id !== index)
        if (newObj.length >= 0) {
            filterApiCall(newObj)
            setFilterObj(newObj)
        }
    }

    const handleAddFilter = () => {

        const newObj = [
            ...filterObj,
            {
                filter_id: addCount++,
                condition: readState.condition,
                column_name: readState.column_name,
                value: readState.value
            }
        ]

        setFilterObj(newObj)
        filterApiCall(newObj)
        setFormModal(!formModal)
    }

    const handleFieldSelect = (optVal) => {

        const filteredUnique = Array.from(
            new Set(rowData.map((item) => item[optVal.value]))
        )

        const selectOptionLists = filteredUnique.map(item => {
            return {
                value: (item !== null && item !== undefined) ? item : 'null',
                label: (item !== null && item !== undefined) ? item : "Null"
            }
        })

        setState(pre => ({ ...pre, column_name: optVal.value, selectOptionList: selectOptionLists }))
    }

    return (
        <Fragment>
            <Modal isOpen={formModal} toggle={() => setFormModal(!formModal)} className='modal-dialog-centered'>
                <ModalHeader toggle={() => setFormModal(!formModal)}>Dynamic Report Filter</ModalHeader>
                <ModalBody>
                    <FormGroup>
                        <Label>Field:</Label>
                        <Select
                            theme={selectThemeColors}
                            className='react-select'
                            classNamePrefix='select'
                            options={availableListRows.map(listVal => {
                                return { value: listVal, label: listVal }
                            })}
                            isClearable={false}
                            onChange={(optVal) => { handleFieldSelect(optVal) }}
                        />
                    </FormGroup>
                    <FormGroup>
                        <Label for='password'>Operator:</Label>
                        <Select
                            theme={selectThemeColors}
                            className='react-select'
                            classNamePrefix='select'
                            options={operatorOptions}
                            value={operatorOptions.find(i => i.value === readState.condition)}
                            isClearable={false}
                            onChange={(optVal) => { handleOperator(optVal) }}
                        />
                    </FormGroup>
                    {
                        readState.field_disabled ? (<FormGroup>
                            <Label>Value:</Label>
                            <CreatableSelect
                                theme={selectThemeColors}
                                className='react-select'
                                classNamePrefix='select'
                                isMulti={true}
                                options={readState.selectOptionList}
                                isClearable={false}
                                onChange={(val) => {
                                    if (val) {

                                        setState(pre => ({ ...pre, value: val.map(valRow => valRow.value) }))

                                        if (val[0].value === 'null') {

                                            let constionCheck = { value: 'is_null', label: 'is null' }

                                            if (readState.condition === 'is') {
                                                constionCheck = { value: 'is_null', label: 'is null' }
                                            } else if (readState.condition === 'is_not') {
                                                constionCheck = { value: 'is_not_null', label: 'is not null' }
                                            }

                                            handleOperator(constionCheck)
                                        }
                                    }
                                }}
                            />
                        </FormGroup>
                        ) : null
                    }
                </ModalBody>
                <ModalFooter>
                    <Button color='primary' onClick={() => handleAddFilter()}>
                        Add Filter
                    </Button>
                </ModalFooter>
            </Modal>

            <Card>
                <CardBody className="p-0">
                    <PerfectScrollbar className="scroll-box-horizontal" options={{ wheelPropagation: true, suppressScrollY: false }}>

                        {
                            (filterObj) ? (
                                filterObj.map((filterVal, index) => {
                                    return <div className='border-primary rounded mx-1 filter-output-box' key={index}>
                                        <span className='ml-1 mr-1'><Badge color="warning">{filterVal.condition}</Badge> <Badge color="primary">{filterVal.column_name}</Badge> <Badge color="dark">{filterVal.value.toString()}</Badge></span> <Button.Ripple className='btn-icon' size='sm' color='flat-danger' onClick={() => { handleRemoveFilter(filterVal.filter_id) }}><X size='15' /></Button.Ripple>
                                    </div>
                                })
                            ) : null
                        }


                        <div className='mx-1 filter-output-box p-0' >
                            <Button.Ripple size='sm' color='primary' outline onClick={() => {
                                setFormModal(!formModal)
                            }}>
                                <Plus size='20' />&nbsp;Add Filter
                            </Button.Ripple>
                        </div>

                    </PerfectScrollbar>
                </CardBody>
                {loading ? <PreLoader /> : null}
            </Card>
        </Fragment>
    )
}

export default HeaderFilter