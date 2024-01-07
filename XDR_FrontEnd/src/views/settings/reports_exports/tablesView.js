
// ================================================================================================
//  File Name: tableViews.js
//  Description: Details of the Dynamic Report.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect, useRef } from 'react'
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardBody, UncontrolledAlert } from 'reactstrap'
import { useSelector, useDispatch } from 'react-redux'
import PreLoader from './preLoader'
import Export from './exports'
import ExpandableTable from './expandableTableView'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { useTranslation } from 'react-i18next'
import axios from '@axios'
import { token } from '@utils'
import { toast } from "react-toastify"
import _debounce from 'lodash/debounce'

const scrollPositionLimit = 20
let scrollPositionOffset = 0

let searchQueryLocal = {
    query: [],
    index_name: '',
    limit: 0,
    time_filter: ''
}

const TablesView = () => {
    const { t } = useTranslation()
    const dataTableRef = useRef(null)

    const dispatch = useDispatch()
    const { loading, selectedList, rowData, searchQuery } = useSelector(state => state.reports_exports)

    const rowsData = rowData.map(obj => Object.fromEntries(Object.entries(obj).filter(([key]) => selectedList.includes(key))))

    searchQueryLocal = { ...searchQueryLocal, ...searchQuery }

    useEffect(() => {
        scrollPositionOffset = 0
    }, [searchQueryLocal.query.length, searchQueryLocal.index_name, searchQueryLocal.time_filter])

    useEffect(() => {

        if (dataTableRef.current) {
            dataTableRef.current.scrollTop = 0
        }

    }, [selectedList.length, searchQueryLocal.index_name, searchQueryLocal.time_filter])

    const scrollApiCall = (offset) => {

        dispatch({ type: 'API_LOADER', loading: true })

        axios.post(`/dynamic-report-filter`, { ...searchQueryLocal, offset }, { headers: { Authorization: token() } })
            .then(res => {

                if (res.data.message_type === "success") {
                    dispatch({ type: 'DYNAMIC_REPORT_BY_SCROLL', scrollData: res.data.data })
                }

                if (res.data.message_type === "d_not_f") {
                    toast.warn("Data Not Found.", {
                        position: "top-right",
                        autoClose: 5000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined
                    })
                }

            })
            .catch(error => {
                toast.warn(error.message, {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined
                })
            })
            .finally(() => {
                dispatch({
                    type: 'API_LOADER',
                    loading: false,
                    errStatus: false,
                    errMsg: ''
                })
            })
    }

    const handleScroll = _debounce(() => {
        const { scrollTop, clientHeight, scrollHeight } = dataTableRef.current

        let scrollPercentage = (scrollTop / (scrollHeight - clientHeight)) * 100
        scrollPercentage = parseInt(scrollPercentage.toFixed())

        if (scrollPercentage >= 99) {
            scrollPositionOffset = scrollPositionOffset += scrollPositionLimit
            scrollApiCall(scrollPositionOffset)
        }
    }, 300)

    useEffect(() => {

        if (dataTableRef.current) {
            dataTableRef.current.addEventListener('scroll', handleScroll)
        }

        return () => {
            if (dataTableRef.current) {
                dataTableRef.current.removeEventListener('scroll', handleScroll)
            }
        }
    }, [])

    const RenderDataTable = () => {

        if (rowData.length > 0) {
            if (selectedList.length > 0) {
                return <>
                    <Export renderCheck={selectedList.length} data={rowsData} />
                    <DataTable
                        noHeader
                        data={rowsData}
                        expandableRows
                        columns={selectedList.map((col => {
                            return {
                                name: `${col}`,
                                cell: (row) => {
                                    return `${row[col]}`
                                },
                                sortable: true
                            }
                        }))}
                        expandOnRowClicked
                        className='react-dataTable'
                        sortIcon={<ChevronDown size={10} />}
                        expandableRowsComponent={ExpandableTable}
                    />
                </>
            } else {
                return <>
                    <DataTable
                        noHeader
                        data={rowData}
                        expandableRows
                        columns={[
                            {
                                name: t('Timestamp'),
                                maxWidth: "250px",
                                cell: row => { return new Date(row['@timestamp']).toString().slice(0, 24) },
                                style: {
                                    fontSize: "1.1em",
                                    fontWeight: "500"
                                }
                            },
                            {
                                name: t('source'),
                                cell: row => `${JSON.stringify(row)}`,
                                style: {
                                    height: "auto !important",
                                    width: "100%",
                                    fontSize: "1.2em"
                                }
                            }
                        ]}
                        expandOnRowClicked
                        className='react-dataTable'
                        sortIcon={<ChevronDown size={10} />}
                        expandableRowsComponent={ExpandableTable}
                    />
                </>
            }
        } else {
            return <>
                <UncontrolledAlert color='warning'>
                    <div className='alert-body'>
                        {('No results match your search criteria')}
                    </div>
                </UncontrolledAlert>
                <h1 className='my-1'>{t('Expand your time range')}</h1>
                <p>{t('One or more of the indices youre looking at contains a date field.Your query may not match anything in the current time range,or there may not be any data at all in the currently selected time range.You can try changing the time range to one which contains data.')}</p>
            </>
        }

    }

    return (
        <Card>
            <CardBody>
                <div className='dynamicReportScrollRef p-0' ref={dataTableRef} >
                    <RenderDataTable />
                </div>
            </CardBody>

            {loading ? <PreLoader /> : null}
        </Card>
    )
}

export default TablesView
