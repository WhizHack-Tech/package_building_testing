// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Alerts ML & DL.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useContext } from 'react'
import { Row, Col } from 'reactstrap'
import Detected from './DetectedThreatType'
import Googlemap from './googleMap'
import Country from './TopScroucecountry'
import City from './City'
import AsnDetails from './ASNDetails'
import Attacker_Ip from './AttackerIPs'
import Target_ip from './TargetIp'
import Target_host_Details from './TargetfrequencyhostDetails'
import Target_port from './TargetPort'
import Attacked_service_Details from './AttackedserviceDetails'
import Target_mac from './TargetMac'
import Attacker_frequency_Details from './AttackerfrequencyDetails'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'

const MLDL = () => {
    return (
        <Fragment>
            <Row className='match-height'>
                <Col xl='4' md='6' sm='6'>
                    <Detected />
                </Col>
                <Col xl='8' md='6' sm='6'>
                    <Googlemap />
                </Col>
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
            {/* <Row>
                <Col>
                <Attacker_Ip />
                </Col>
            </Row> */}
            <Row className='match-height'>
                <Col xl='5' sm='12'>
                <Target_port />
                </Col>
                <Col xl='7' sm='12'>
                <Attacked_service_Details />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col xl='7' sm='12'>
                <Target_host_Details />
                </Col>
                <Col xl='5' sm='12'>
                <Target_ip />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col xl='5' sm='12'>
                <Target_mac />
                </Col>
                <Col xl='7' sm='12'>
                <Attacker_frequency_Details />
                </Col>
            </Row>
        </Fragment>
    )
}

export default MLDL
