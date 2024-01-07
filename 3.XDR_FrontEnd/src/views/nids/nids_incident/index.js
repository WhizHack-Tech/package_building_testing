// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Incidents.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment, useContext } from 'react'
import { Row, Col, Spinner } from 'reactstrap'
import { useSelector } from "react-redux"
import Breadcrumbs from '@components/breadcrumbs/incidents_chart'
import CriticalThreats from './CriticalThreats'
import External from './externalattack'
import Internal from './InternalCompromise'
import Lateral from './LateralMovement'
import Attackedhost from './AttackedHostDetails'
import AttackCount from './AttackCountlines'
import ServiceNames from './ServiceNames'
import Cities from './TopAttackerPorts'
import ThreatClass from './ThreatClass'
import Malware from './MalwareType'
import MitraTactick from './MitraTactickName'
import MitraTechnique from './MitraTechniqueName'
import AttackerIPS from './AtaackerTaregtipslines'
import Tabspages from './Tabspages'
import External_vs_Internal from './External_vs_Internal'
import { ThemeColors } from '@src/utility/context/ThemeColors'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'
// ** Custom Hooks
import { useRTL } from '@hooks/useRTL'
// import { ThemeColors } from '@src/utility/context/ThemeColors'
import NotAuthorizedInner from '@src/views/notAuthorizedInner'
const StatisticsCards = () => {
    const [isRtl, setIsRtl] = useRTL()
    const { colors } = useContext(ThemeColors)

    const pagePermissionStore = useSelector((store) => store.pagesPermissions)
    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} color="primary"/></div>
        )
    } else {
        if (pagePermissionStore.env_nids === false) {
            return <NotAuthorizedInner />
        }
    }
    
    return (
        <Fragment>
            <Breadcrumbs breadCrumbTitle="NIDS Incident" />
            <Row className='match-height'>
                <Col xl='6' md='4' sm='6'>
                    <CriticalThreats />
                </Col>
                <Col lg='2' md='6' xs='12'>
                    <Internal />
                </Col>
                <Col lg='2' md='6' xs='12'>
                    <External />
                </Col>
                <Col lg='2' md='6' xs='12'>
                    <Lateral />
                </Col>
            </Row>
            <Col md='12' xs='12'>
                <Row className='match-height' >
                    <Col lg='4' md='12' xs='12'>
                        <Attackedhost />
                        <External_vs_Internal success={colors.success.main} />
                    </Col>
                    <Col lg='8' md='12' xs='12'>
                        <AttackCount direction={isRtl ? 'rtl' : 'ltr'} />
                        <AttackerIPS />
                    </Col>
                </Row>
            </Col>
            {/* <Row>
                <Col lg='4' md='12' xs='12'>
                    <Attackedhost />
                </Col>
                <Col lg='8' md='12' xs='12'>
                    <AttackCount direction={isRtl ? 'rtl' : 'ltr'} />
                </Col>
            </Row> */}
            <Row className='match-height'>
                <Col sm='4'>
                    <ServiceNames />
                </Col>
                <Col sm='4'>
                    <Cities />
                </Col>
                <Col sm='4'>
                    <ThreatClass />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col sm='4'>
                    <Malware />
                </Col>
                <Col sm='4'>
                    <MitraTactick />
                </Col>
                <Col sm='4'>
                    <MitraTechnique />
                </Col>
            </Row>
            <Row>
                <Col>
                    <Tabspages />
                </Col>
            </Row>

        </Fragment>
    )
}

export default StatisticsCards
