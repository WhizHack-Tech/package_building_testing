// ================================================================================================
//  File Name: iframeMap.js
//  Description: Details of the Live Map.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React, { Fragment, useState } from "react"
import { isUserLoggedIn, getUserData } from '@utils'
import { Card, CardBody, CardHeader, CardTitle } from "reactstrap"
import { useSelector } from "react-redux"
import PreLoader from "./preLoader"
import DataNotFound from "../nids/nids_alerts/dNotf"
import { FullScreen, useFullScreenHandle } from "react-full-screen"
import { Link } from 'react-router-dom'
import axios from "@axios"
import { Maximize } from 'react-feather'
import { useTranslation } from 'react-i18next'
const styles = {
    iframeBox: {
        width: '100%',
        height: "100vh",
        border: 'none',
        overflow: "hidden",
        content: 'middle'
    }
}

const RenderMap = ({ apiData }) => {

    const { errorMsg, errorCheck, data } = apiData

    return (
        <React.Fragment>
            <CardBody className="p-0">
                {errorCheck ? (
                    <DataNotFound msg={errorMsg} />
                ) : (
                    <iframe style={styles.iframeBox} src={data}></iframe>
                )}
            </CardBody>
        </React.Fragment>
    )
}

const IframeMap = () => {
    const { t } = useTranslation()
    const handle = useFullScreenHandle()
    const [apiData, setApiData] = useState({
        loading: false,
        data: "",
        errorMsg: "",
        errorCheck: false
    })

    const filterState = useSelector((store => store.dashboard_chart))

    const getApi = () => {
        setApiData(pre => ({ ...pre, loading: true }))
        axios.get(`/live-map-view?location_id=${getUserData().location_id}&activated_plan_id=${getUserData().activated_plan_id}&conditions=${filterState.values ? filterState.values : 'last_1_hour'}`, {
            responseType: 'blob'
        }).then(res => {
            const data = URL.createObjectURL(res.data)
            setApiData(pre => ({ ...pre, loading: false, data, errorCheck: false }))
        }).catch(error => {
            setApiData(pre => ({ ...pre, loading: false, errorMsg: error.message, errorCheck: true }))
        })
    }


    React.useEffect(() => {
        getApi()
    }, [isUserLoggedIn(), filterState.values, filterState.refreshCount])

    return (
        <Fragment>
            <h5>Full Screen &nbsp;&nbsp;
                <Link color='primary' onClick={handle.enter} >
                    <Maximize size={20} />
                </Link>
            </h5>
            <FullScreen handle={handle}>
                <Card className="p-0">
                    <RenderMap apiData={apiData} />
                    {apiData.loading && <PreLoader />}
                </Card>
            </FullScreen>
        </Fragment>
    )
}

export default IframeMap