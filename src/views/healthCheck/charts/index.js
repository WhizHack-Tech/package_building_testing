// ================================================================================================
//  File Name: index.js
//  Description: Details of the Health Check.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useContext, useEffect, useMemo, useState } from 'react'
import { Col, Row } from 'reactstrap'
import { useLocation } from 'react-router-dom'
import { Cpu, Server, Activity } from 'react-feather'

import { ThemeColors } from '@src/utility/context/ThemeColors'
import StatsHorizontal from '@components/widgets/stats/StatsHorizontal'
import axios from '@axios'
import { token } from '@utils'
import { useTranslation } from 'react-i18next'
import Health from './Health'
import TableDataRender from './tableData'
import LineCharRender from './LineChart'
import PreLoader from '../preLoader'


const HealthDetails = () => {
    const {t} = useTranslation()
    const context = useContext(ThemeColors)
    const { search } = useLocation()
    const searchParams = useMemo(() => new URLSearchParams(search), [search])

    const [sysData, setSysData] = useState({
        cpu_utilization: 0,
        disk_remaining: 0,
        ram_utilization: 0,
        apiLoader: false,
        apiErrMsg: ""
    })

    const [sysDataTable, setSysDataTable] = useState({
        tableData: [],
        apiLoader: false,
        apiErrMsg: ""
    })

    const [lineChart, setLineChart] = useState({
        total: 0,
        shortTableData: [],
        running: [],
        stop: [],
        apiLoader: false,
        apiErrMsg: ""
    })

    const apiSysData = () => {
        setSysData(pre => ({ ...pre, apiLoader: true, apiErrMsg: "" }))

        axios.get(`/hc-dynamic-latest-info?sensor_type=${searchParams.get('sensor_type')}`,
            { headers: { Authorization: token() } }).then(res => {
                setSysData(pre => ({ ...pre, apiLoader: false }))

                if (res.data.message_type === "success") {

                    setSysData(pre => ({
                        ...pre,
                        cpu_utilization: res.data.data.cpu_utilization,
                        disk_remaining: res.data.data.disk_remaining,
                        ram_utilization: res.data.data.ram_utilization
                    }))

                }

            })
            .catch(err => {
                setSysData(pre => ({ ...pre, apiLoader: false, apiErrMsg: err.message }))
            })
    }

    const apiSysDataTable = () => {
        setSysDataTable(pre => ({ ...pre, apiLoader: true, apiErrMsg: "" }))

        axios.get(`/hc-feeds-table?sensor_type=${searchParams.get('sensor_type')}&sensor_id=${searchParams.get('sensor_id')}&current_time=${searchParams.get('current_time')}&past_time=${searchParams.get('past_time')}`,
            { headers: { Authorization: token() } }).then(res => {
                setSysDataTable(pre => ({ ...pre, apiLoader: false }))

                if (res.data.message_type === "success") {

                    setSysDataTable(pre => ({
                        ...pre,
                        tableData: res.data.table
                    }))

                }

            })
            .catch(err => {
                setSysDataTable(pre => ({ ...pre, apiLoader: false, apiErrMsg: err.message }))
            })
    }

    const apiLineChart = () => {
        setLineChart(pre => ({ ...pre, apiLoader: true, apiErrMsg: "" }))

        axios.get(`/hc-level-line-chart?sensor_type=${searchParams.get('sensor_type')}&sensor_id=${searchParams.get('sensor_id')}&current_time=${searchParams.get('current_time')}&past_time=${searchParams.get('past_time')}&condition=${searchParams.get('condition')}`,
            { headers: { Authorization: token() } }).then(res => {
                setLineChart(pre => ({ ...pre, apiLoader: false }))

                if (res.data.message_type === "success") {

                    setLineChart(pre => ({
                        ...pre,
                        total: res.data.total,
                        shortTableData: res.data.filter,
                        running: res.data.running,
                        stop: res.data.stop
                    }))

                }

            })
            .catch(err => {
                setLineChart(pre => ({ ...pre, apiLoader: false, apiErrMsg: err.message }))
            })
    }

    useEffect(() => {
        apiSysData()
        apiSysDataTable()
        apiLineChart()
    }, [])

    return (
        <Fragment>
            <Row className='match-height'>
                {/* <Col lg='2' md='2'>
                    <Row className='match-height'>
                        <Col md='12'>
                            <Health primary={context.colors.primary.main} danger={context.colors.danger.main} />

                        </Col>
                        <Col md='12'>
                            <Health primary={context.colors.primary.main} danger={context.colors.danger.main} />

                        </Col>
                    </Row>
                </Col> */}

                <Col lg='12' md='12'>
                    <Row className='match-height'>
                        <Col lg='4' md='3' xs='6'>
                            <StatsHorizontal icon={<Server size={21} />} color='warning' stats={`${sysData.disk_remaining} %`} statTitle= {t('Disk Remaining')} />
                            {sysData.apiLoader ? <PreLoader /> : null}
                        </Col>
                        <Col lg='4' md='3' xs='6'>
                            <StatsHorizontal icon={<Cpu size={21} />} color='danger' stats={`${sysData.cpu_utilization} %`} statTitle={t('CPU Utilization')} />
                            {sysData.apiLoader ? <PreLoader /> : null}
                        </Col>
                        <Col lg='4' md='3' xs='6'>
                            <StatsHorizontal icon={<Activity size={21} />} color='primary' stats={`${sysData.ram_utilization} %`} statTitle={t('RAM Used')} />
                            {sysData.apiLoader ? <PreLoader /> : null}
                        </Col>
                        <Col lg='12' md='12' xs='12'>
                            <LineCharRender lineChart={lineChart} />
                            {lineChart.apiLoader ? <PreLoader /> : null}
                        </Col>
                    </Row>
                </Col>
                <Col md='12'>
                    <TableDataRender tableData={sysDataTable.tableData} />
                    {sysDataTable.apiLoader ? <PreLoader /> : null}
                </Col>
            </Row>
        </Fragment>
    )
}

export default HealthDetails