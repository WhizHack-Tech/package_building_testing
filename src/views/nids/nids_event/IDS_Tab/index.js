// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Events IDS Pages.
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
// import Attacker_Ip from './AttackerIPs'
import Target_ip from './TargetIp'
import Attacker_frequency from './AttackerfrequencyDetails'
import Target_port from './TargetPort'
import Attacker_service from './Attackerservicedetails'
import Target_mac from './TargetMac'
import Target_host_Details from './Taregethostdetails'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'

const StatisticsCards = () => {
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
                <Col lg='12' md='12' xs='12'>
                    <Attacker_Ip />
                </Col>
            </Row> */}
            <Row className='match-height'>
                <Col xl='5' sm='12'>
                    <Target_port />
                </Col>
                <Col xl='7' sm='12'>
                    <Attacker_service />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col xl='7' sm='12'>
                    <Attacker_frequency />
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
                    <Target_host_Details />
                </Col>
            </Row>
        </Fragment>
    )
}

export default StatisticsCards
