// ================================================================================================
//  File Name: iframeMap.js
//  Description: Details of the Soar Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React, { useState } from "react"
import { Card, CardBody, CardHeader, CardTitle } from "reactstrap"
import PreLoader from "./preLoader"
import DataNotFound from "../nids/nids_alerts/dNotf"
import { FullScreen, useFullScreenHandle } from "react-full-screen"
import { Link } from 'react-router-dom'
import axios from "@axios"
import { Maximize } from 'react-feather'

const styles = {
    iframeBox: {
        width: '100%',
        height: "100vh",
        border: 'none',
        overflow: "hidden",
        content: 'middle'
    }
}

const _URL = "https://xdr-demo-response.zerohack.in/login"
// const _URL = "http://localhost:3002/components/modals"

const RenderMap = ({ apiData }) => {

    const { errorMsg, errorCheck, data } = apiData

    return (
        <React.Fragment>
            <iframe style={styles.iframeBox} src={_URL}></iframe>
            {/* <CardBody className="p-0">
                {errorCheck ? (
                    <DataNotFound msg={errorMsg} />
                ) : (
                    <iframe style={styles.iframeBox} src={data}></iframe>
                )}
            </CardBody> */}
        </React.Fragment>
    )
}

const IframeMap = () => {
    const handle = useFullScreenHandle()
    const [apiData, setApiData] = useState({
        loading: false,
        data: "",
        errorMsg: "",
        errorCheck: false
    })

    const getApi = () => {
        setApiData(pre => ({ ...pre, loading: true }))

        // window.open(_URL, '_blank')
        axios.get(_URL, {
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
    }, [])

    return (
        <Card className="p-0">
            <CardHeader className='pt-2 pl-2 d-flex justify-content-between align-items-sm-center align-items-start flex-sm-row flex-column'>
            </CardHeader>

            <CardBody className="px-2 pb-2">
                <RenderMap apiData={apiData} />
            </CardBody>
            {apiData.loading && <PreLoader />}
        </Card>
    )
}

export default IframeMap