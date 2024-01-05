import { Fragment, useContext } from "react"
import { Col, Row, Card } from 'reactstrap'
import CriticalThreats from './CriticalThreats'
import InternalAttacks from './InternalAttacks'
import OutgoingBotnet from './OutgoingBotnet'
import Externalattacks from './ExternalAttacks'
import Threat from './TreatsLogs'
import Detectiontype from './DetectedThreatType'
import Overallattack from './OverallAttack'
import Internal from './InternalExternal'
import Topattacks from './TopAttacks'
import Topattack from './TopsourceAttackCountries'
import Google from './googleMap'
import Citypie from './TopAttackerCities'
import ASN_Details from './TopAttackerASNs'
import AttackerIps from './AttackerIPs'
import Mostattackedports from './MostAttackedPorts'
import Demograph from './Demograph'
import Breadcrumbs from '@components/breadcrumbs/nids_charts'
import { ThemeColors } from '@src/utility/context/ThemeColors'
import { useSkin } from '@hooks/useSkin'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'


const Dashboards = () => {

    // const context = useContext(ThemeColors),
    // const { context } = useContext(ThemeColors),
    const { context, colors } = useContext(ThemeColors),
        [skin, setSkin] = useSkin(),
        labelColor = skin === 'dark' ? '#b4b7bd' : '#6e6b7b',
        tooltipShadow = 'rgba(0, 0, 0, 0.25)',
        gridLineColor = 'rgba(200, 200, 200, 0.2)',
        lineChartPrimary = '#666ee8',
        lineChartDanger = '#ff4961',
        warningColorShade = '#ffe802',
        warningLightColor = '#FDAC34',
        successColorShade = '#28dac6',
        yellowColor = '#ffe800'
    return (
        <Fragment>
            <Breadcrumbs breadCrumbTitle="NIDS" />
            <Row>
                <Col lg='3' md='6' xs='12'>
                    <CriticalThreats />
                </Col>
                <Col lg='3' md='6' xs='12'>
                    <InternalAttacks />
                </Col>
                <Col lg='3' md='6' xs='12'>
                    <OutgoingBotnet />
                </Col>
                <Col lg='3' md='6' xs='12'>
                    <Externalattacks />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col lg='8' md='6' xs='12'>
                    <Threat />
                </Col>
                <Col lg='4' md='6' xs='12'>
                    <Detectiontype />
                </Col>
            </Row>
            <Row className='match-height'>
                <Col lg='4' md='12' xs='12'>
                    <Overallattack />
                </Col>
            </Row>
            <h4>Events</h4>
            <Row>
                <Col>
                    <Topattacks cols={{ md: '3', sm: '6' }} />
                </Col>
            </Row>
            <div>
                <Row className='match-height'>
                    <Col lg='6' md='12' xs='12'>
                        <Topattack
                            info={colors.info.main}
                            labelColor={labelColor}
                            tooltipShadow={tooltipShadow}
                            gridLineColor={gridLineColor}
                        />
                    </Col>
                    <Col lg='6' md='12' xs='12'>
                        <Google />
                    </Col>
                </Row>
                <Row className='match-height'>
                    <Col lg='4' md='12' xs='12'>
                        <Citypie />
                    </Col>
                    <Col lg='8' md='12' xs='12'>
                        <ASN_Details
                            successColorShade={successColorShade}
                            labelColor={labelColor}
                            tooltipShadow={tooltipShadow}
                            gridLineColor={gridLineColor}
                            lineChartPrimary={lineChartPrimary}
                            yellowColor={yellowColor}
                        />
                    </Col>
                </Row>
                <Row className='match-height'>
        <Col lg='8' md='12' xs='12'>
         <AttackerIps />
        </Col>
        <Col lg='4' md='12' xs='12'>
          <Mostattackedports
            tooltipShadow={tooltipShadow}
            successColorShade={successColorShade}
            warningLightColor={warningLightColor}
            primary={colors.primary.main}
          />
        </Col>
      </Row>
      <Row>
      <Col lg='2' sm='2'>
          <Demograph />
        </Col>
      </Row>
            </div>
        </Fragment>
    )
}
export default Dashboards