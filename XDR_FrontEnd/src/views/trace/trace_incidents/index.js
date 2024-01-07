// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Incidents Pages ). 
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useContext } from 'react'
import { Col, Row, Spinner } from 'reactstrap'
import { useSelector } from "react-redux"
import Critical from './CriticalThreats'
import Lateral from './LateralMovement'
import Map from './googleMap'
import Internal from './InternalCompromise'
import External from './externalattack'
import Typethreat from './Typeofthreat'
import AttackerPort from './AttackerPorts'
import Attackerips from './AtaackerTaregtipslines'
import Could from './Couldchart1'
import Could1 from './Couldchart2'
import Could2 from './Couldchart3'
import Country from './TopScroucecountry'
import City from './City'
import AsnDetails from './ASNDetails'
import Target from './TargetPort'
import Attckedservice from './Attackerservicedetails'
import Attackfrequency from './AttackerfrequencyDetails'
import Targrtip from './TargetIp'
import Breadcrumbs from '@components/breadcrumbs/nids_charts'
//SCSS//
import { ThemeColors } from '@src/utility/context/ThemeColors'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import NotAuthorizedInner from '@src/views/notAuthorizedInner'

const DatabaseServer = () => {
    const { colors } = useContext(ThemeColors)
    
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
            <Breadcrumbs breadCrumbTitle="TRACE Incidents" />
            <Row className='match-height'>
                <Col lg='9' md='6' xs='12' style={{ height: '180px' }}>
                    <Critical />
                </Col>
                <Col lg='3' md='6' xs='12'>
                    <Lateral />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col lg='9' md='6' xs='12' style={{ height: '590px' }}>
                    <Map />
                </Col>
                <Col lg='3' md='6' xs='12'>
                    <External />
                    <Internal />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col lg='3' md='6' xs='12'>
                    <Typethreat success={colors.success.main} />
                    <AttackerPort />
                </Col>
                <Col lg='9' md='6' xs='12'>
                    <Attackerips />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col sm='6'>
                    <Could />
                </Col>
                <Col sm='6'>
                    <Could1 />
                </Col>
                {/* <Col sm='4'>
                    <Could2 />
                </Col> */}
            </Row>
            <Row className='match-height'>
                <Col xl='4' sm='12'>
                    <Country />
                </Col>
                <Col xl='4' sm='12'>
                    <City />
                </Col>
                <Col xl='4' sm='12'>
                    <AsnDetails />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col xl='4' sm='12'>
                    <Target />
                </Col>
                <Col xl='8' sm='12'>
                    <Attckedservice />
                </Col>
            </Row>
             <Row className='match-height'>
                <Col xl='8' sm='12'>
                    <Attackfrequency />
                </Col>
                <Col xl='4' sm='12'>
                    <Targrtip />
                </Col>
            </Row>
        </Fragment>
    )
}

export default DatabaseServer