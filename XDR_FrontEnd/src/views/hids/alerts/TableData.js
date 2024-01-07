// ================================================================================================
//  File Name:  TableData.js
//  Description: Details of the HIDS Table.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React, { Fragment, useEffect, useState, memo } from 'react'
import { ChevronDown, Eye } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle, Badge, CardBody, Input, Label, Row, Col } from 'reactstrap'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { token } from '@utils'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { useTranslation } from 'react-i18next'
import { useSelector } from 'react-redux'
import PreLoader from '../preLoader'
import DataNotFound from '../dNotf'

const TablesData = () => {
    const { t } = useTranslation()
    const [tableData, setTableData] = useState([])
    const [apiLoader, setApiLoader] = useState(false)
    const filterState = useSelector((store => store.dashboard_chart))
    const [checkApiData, setCheckApiData] = useState(true)
    const [searchValue, setSearchValue] = useState('')

    const DetailsApiLogic = () => {
        setApiLoader(true)
        axios.get(`/show-unique-agent-id?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
            .then(res => {
                setApiLoader(false)

                if (res.data.message_type === "d_not_f") {
                    setCheckApiData(false)
                }

                if (res.data.message_type === "success") {
                    setCheckApiData(true)
                    setTableData(res.data.data)
                }

            })
            .catch(error => {
                setApiLoader(false)
                console.log(error.message)
            })
    }

    useEffect(() => {
        DetailsApiLogic()
    }, [filterState.values, filterState.refreshCount])

    const handleSearch = e => {
        setSearchValue(e.target.value.trim())
    }

    const filteredData = tableData.filter(item => {
        const agentId = String(item.agent_id)
        const agentName = String(item.agent_name)
        const agentIp = String(item.agent_ip)

        return (
            agentId.toLowerCase().includes(searchValue.toLowerCase()) ||
            agentName.toLowerCase().includes(searchValue.toLowerCase()) ||
            agentIp.toLowerCase().includes(searchValue.toLowerCase())
        )
    })

    const basicColumns = [
        {
            name: t('Agent ID'),
            selector: 'agent_id',
            sortable: true,
            maxWidth: '400px'
        },
        {
            name: t('Name'),
            selector: 'agent_name',
            sortable: true
        },
        {
            name: t('IP'),
            selector: 'agent_ip',
            sortable: true
        },
        {
            name: t('Actions'),
            selector: 'action',
            cell: rowData => {
                return <Link to={`/hids-alert-details?current_time=${rowData.current_time}&past_time=${rowData.past_time}&agent_id=${rowData.agent_id}&condition=${rowData.condition}`}>
                    <Eye />
                </Link>
            }
        }
    ]

    return (
        <Fragment>
            <Card>
                <CardHeader>
                    <CardTitle tag='h2'>{t('Alert')}</CardTitle>
                </CardHeader>
                <Row className='justify-content-end mx-0'>
                    <Col className='d-flex align-items-center justify-content-end' md='3' sm='6'>
                        <Input
                            type='text'
                            placeholder={t('Search')}
                            className='form-control'
                            value={searchValue}
                            onChange={handleSearch}
                        />
                    </Col>
                </Row>
                <CardBody>
                    {checkApiData ? (
                        <div className='react-dataTable'>
                            <DataTable
                                noHeader
                                pagination
                                data={filteredData}
                                columns={basicColumns}
                                className='react-dataTable'
                                sortIcon={<ChevronDown size={5} />}
                                paginationPerPage={5}
                                paginationRowsPerPageOptions={[5, 10, 25, 50, 100]}
                            />
                        </div>
                    ) : (
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                            <p>{t('Data Not Found')}</p>
                        </div>
                    )}
                </CardBody>
                {apiLoader ? <PreLoader /> : null}
            </Card >
        </Fragment>
    )
}

export default memo(TablesData)
