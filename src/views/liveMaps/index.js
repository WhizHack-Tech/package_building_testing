// ================================================================================================
//  File Name: Index.js
//  Description: Details of the Live Map.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React from "react"
import { Spinner } from 'reactstrap'
import { useSelector } from "react-redux"
import IframeMap from "./iframeMap"
import Breadcrumbs from '@components/breadcrumbs/nids_charts'
import NotAuthorizedInner from '@src/views/notAuthorizedInner'

const Maps = () => {

    const pagePermissionStore = useSelector((store) => store.pagesPermissions)
    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} color="primary" /></div>
        )
    } else {
        if (pagePermissionStore.xdr_live_map === false) {
            return <NotAuthorizedInner />
        }
    }

    return (
        <React.Fragment>
            <Breadcrumbs breadCrumbTitle="Live Map" />
            <IframeMap />
        </React.Fragment>
    )
}

export default Maps