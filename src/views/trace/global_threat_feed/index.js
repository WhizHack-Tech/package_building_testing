// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Golbal Threat Feed ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, React } from "react"
import { Col, Row, Spinner } from 'reactstrap'
import { useSelector } from "react-redux"
import Malware from './Malware'
import Intel from './Intelsource'
import Threat from './Threattype'
import Breadcrumbs from '@components/breadcrumbs/global_charts'
import Table from './Table'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import NotAuthorizedInner from '@src/views/notAuthorizedInner'

const Dashboard = () => {
    
    const pagePermissionStore = useSelector((store) => store.pagesPermissions)
    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} color="primary"/></div>
        )
    } else {
        if (pagePermissionStore.env_trace === false) {
            return <NotAuthorizedInner />
        }
    } 

    return (
        <Fragment>
            <Breadcrumbs breadCrumbTitle="Global Threat Feed" />
            <Row className='match-height'>
            <Col xl='4' md='4' sm='6'>
                    <Malware />
                </Col>
                <Col xl='4' md='4' sm='6'>
                    <Intel />
                </Col>
                <Col xl='4' md='4' sm='6'>
                    <Threat />
                </Col>
            </Row>
            <Row>
                <Col>
                    <Table />
                </Col>
            </Row>
        </Fragment>
    )
}

export default Dashboard