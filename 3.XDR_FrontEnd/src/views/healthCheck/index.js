import React, { useState, useEffect } from 'react'
import {
    TabContent,
    TabPane,
    Nav,
    NavItem,
    NavLink,
    Spinner,
    Card
} from 'reactstrap'
import { useSelector } from "react-redux"
import Breadcrumbs from '@components/breadcrumbs/health_sensor'
import NotAuthorizedInner from '@src/views/notAuthorizedInner'
import axios from '@axios'
import { token } from '@utils'
import PreLoader from './preLoader'
import TablesDAta from "./tables"
import { useTranslation } from 'react-i18next'
let checkTabClickStatus = false
let checkTabClickeValue = ""

const HealthCheck = () => {
    const { t } = useTranslation()
    const pagePermissionStore = useSelector((store) => store.pagesPermissions)
    const filterState = useSelector((store => store.health_sensor))
    const [active, setActive] = useState('trace')
    const [apiData, setApiData] = useState({
        trace: false,
        nids: false,
        hids: false,
        soar: false,
        traceData: [],
        nidsData: [],
        hidsData: [],
        soarData: [],
        pastTime: 0,
        currentTime: 0,
        apiLoader: false,
        apiErrMsg: ""
    })

    const toggle = tab => {
        setActive(tab)
        checkTabClickStatus = true
        checkTabClickeValue = tab
    }

    const getApi = () => {

        setApiData(pre => ({ ...pre, apiLoader: true, apiErrMsg: "" }))

        axios.get(`/hc-status-all-products?condition=${filterState.values ? filterState.values : 'last_7_days'}`,
            { headers: { Authorization: token() } }).then(res => {
                setApiData(pre => ({ ...pre, apiLoader: false }))

                if (res.data.message_type === "success") {

                    setApiData(pre => ({
                        ...pre,
                        trace: res.data.trace,
                        nids: res.data.nids,
                        hids: res.data.hids,
                        soar: res.data.soar,
                        traceData: res.data.data.trace,
                        nidsData: res.data.data.nids,
                        hidsData: res.data.data.hids,
                        soarData: res.data.data.soar,
                        pastTime: res.data.filter.past_time,
                        currentTime: res.data.filter.current_time
                    }))

                    let checkTabAcive = ""
                    if (res.data.trace) {
                        checkTabAcive = 'trace'
                    } else if (res.data.nids) {
                        checkTabAcive = 'nids'
                    } else if (res.data.hids) {
                        checkTabAcive = 'hids'
                    } else if (res.data.soar) {
                        checkTabAcive = 'soar'
                    }

                    if (checkTabClickStatus === false) {
                        setActive(checkTabAcive)
                    } else {
                        setActive(checkTabClickeValue)
                    }

                }

            })
            .catch(err => {
                setApiData(pre => ({ ...pre, apiLoader: false, apiErrMsg: err.message }))
            })
    }

    useEffect(() => {
        getApi()
    }, [filterState.values, filterState.refreshCount])

    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} color="primary" /></div>
        )
    } else {
        if (pagePermissionStore.env_hc === false) {
            return <NotAuthorizedInner />
        }
    }

    return (
        <React.Fragment>
            <Breadcrumbs breadCrumbTitle='Sensor Health' />
            <Nav pills className='d-flex justify-content-center align-items-center mb-1'>
                {
                    apiData.trace ? <NavItem>
                        <NavLink
                            active={active === 'trace'}
                            onClick={() => {
                                toggle('trace')
                            }}
                        >
                            {t('TRACE')}
                        </NavLink>
                    </NavItem> : null
                }

                {
                    apiData.nids ? <NavItem>
                        <NavLink
                            active={active === 'nids'}
                            onClick={() => {
                                toggle('nids')
                            }}
                        >
                            {t('NIDS')}
                        </NavLink>
                    </NavItem> : null
                }

                {
                    apiData.hids ? <NavItem>
                        <NavLink
                            active={active === 'hids'}
                            onClick={() => {
                                toggle('hids')
                            }}
                        >
                            {t('HIDS')}
                        </NavLink>
                    </NavItem> : null
                }

                {
                    apiData.soar ? <NavItem>
                        <NavLink
                            active={active === 'soar'}
                            onClick={() => {
                                toggle('soar')
                            }}
                        >
                            {t('SOAR')}
                        </NavLink>
                    </NavItem> : null
                }

            </Nav>
            <Card>
                <TabContent className='py-50' activeTab={active}>
                    <TabPane tabId='trace'>
                        <TablesDAta tableTitle={t("TRACE Health Check")} tableData={apiData.traceData} pastTime={apiData.pastTime} currentTime={apiData.currentTime} filteCondition={filterState.values ? filterState.values : 'last_1_hour'} />
                    </TabPane>
                    <TabPane tabId='nids'>
                        <TablesDAta tableTitle={t("NIDS Health Check")} tableData={apiData.nidsData} pastTime={apiData.pastTime} currentTime={apiData.currentTime} filteCondition={filterState.values ? filterState.values : 'last_1_hour'} />
                    </TabPane>
                    <TabPane tabId='hids'>
                        <TablesDAta tableTitle={t("HIDS Manager")} tableData={apiData.hidsData} pastTime={apiData.pastTime} currentTime={apiData.currentTime} filteCondition={filterState.values ? filterState.values : 'last_1_hour'} />
                    </TabPane>
                    <TabPane tabId='soar'>
                        <TablesDAta tableTitle={t("SOAR Health Check")} tableData={apiData.soarData} pastTime={apiData.pastTime} currentTime={apiData.currentTime} filteCondition={filterState.values ? filterState.values : 'last_1_hour'} />
                    </TabPane>
                </TabContent>
                {apiData.apiErrMsg ? <p className='text-center'>{apiData.apiErrMsg}</p> : null}
                {apiData.apiLoader ? <PreLoader /> : null}
            </Card>
        </React.Fragment>
    )
}

export default HealthCheck