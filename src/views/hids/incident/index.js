// ================================================================================================
//  File Name: index.js
//  Description: Details of the HIDS Incident Graph.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import TablesData from "./TableData"
import MitePicdss from "./MitePicdss"
import MitraTactick from './MitraTactickName'
import MitraTechnique from './MitraTechniqueName'
import AnomolyDetection from './AnomolyDetection'
import Ransomware from './RansomwareDetection'
import { Row, Col, Spinner } from "reactstrap"
import { useSelector } from "react-redux"
import { Fragment, useContext } from "react"
import Breadcrumbs from '@components/breadcrumbs/incidents_chart'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { ThemeColors } from '@src/utility/context/ThemeColors'
import NotAuthorizedInner from '@src/views/notAuthorizedInner'

const Hidsalert = () => {
    const { colors } = useContext(ThemeColors)

    const pagePermissionStore = useSelector((store) => store.pagesPermissions)
    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} color="primary" /></div>
        )
    } else {
        if (pagePermissionStore.env_hids === false) {
            return <NotAuthorizedInner />
        }
    }

    return (
        <Fragment>
            <Breadcrumbs breadCrumbTitle="HIDS Incident" />
            <Row className='match-height'>
            <Col xl='2' md='4' sm='4'>
                    <AnomolyDetection />
                    <Ransomware />
                </Col>
                <Col xl='5' md='4' sm='4'>
                    <MitraTactick />
                </Col>
                <Col xl='5' md='4' sm='4'>
                    <MitePicdss />
                </Col>
            </Row>
            <Row className='match-height'>
            <Col xl='4' md='4' sm='4'>
                    <MitraTechnique />
                </Col>
                <Col xl='8' md='12' sm='12'>
                    <TablesData />
                </Col>
            </Row>
        </Fragment>
    )
}

export default Hidsalert  