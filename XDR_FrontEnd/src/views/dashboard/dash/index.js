// Filename : index.js
// Purpose/Description : This page collecting data from dashboard folder and showing in the page after importing the pages 
// Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
// Copyright (c) : Whizhack Technologies (P) Ltd.

import { Fragment, useContext, useEffect } from 'react'
import { Row, Col } from 'reactstrap'
import Breadcrumbs from '@components/breadcrumbs'
import ThreatLogs from './ThreatLogs'
import Internalattck from './Internalattck'
import External from './External'
import Pie from './Pie'
import Severity from './Severity1'
import Leteral from './Lateral'
import Detectiontype from './Detectiontype'
// import Newgraph from './Newgraph'
import { ThemeColors } from '@src/utility/context/ThemeColors'
import Internal_vs_external from './Internal_vs_external'
import { useSkin } from '@hooks/useSkin'
import { dashboar_charts, dashboar_filter } from "../../../redux/actions/charts/dashboard_charts"
import { useDispatch, useSelector } from "react-redux"
import { addDays, format } from "date-fns"
import { useTranslation } from 'react-i18next'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'
import axios from '@axios'
import { token } from '@utils'
import { WsCheck, wsCon, wsReCon, wsDis } from '../../../ws_con'

const platform = [
  { value: 'aws', label: 'AWS', color: '#00B8D9', isFixed: true},
  { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true},
  { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true}
]

const severity = [
  { value: '1', label: 'High', color: '#00B8D9'},
  { value: '2', label: 'Medium', color: '#0052CC'},
  { value: '3', label: 'Low', color: '#5243AA'}
]

const find_default_val = (defaultVal, flagData, checkInt = false) => {

  let finalData = {
    defaultVals : [],
    values: [],
    labels: []
  }

  if (defaultVal !== undefined) {
    defaultVal = defaultVal.split(",")
    for (let p = 0; p < Object.keys(flagData).length; p++) {
      for (let i = 0; i < defaultVal.length; i++) {
        if (flagData[p].value === defaultVal[i]) {
          if (checkInt) {
            finalData.values[i] = parseInt(flagData[p].value)
          } else {
            finalData.values[i] = flagData[p].value
          }

          finalData.defaultVals[i] = flagData[p]
          finalData.labels[i] = flagData[p].label
        }
      }
    }    
  }

  return finalData
}

const StatisticsCards = () => {
  const {t} = useTranslation()
  const dispatch = useDispatch()
  const chart_data = useSelector((store) => store.dashboard_charts.charts)
  const context = useContext(ThemeColors),
    [skin, setSkin] = useSkin(),
    labelColor = skin === 'dark' ? '#b4b7bd' : '#6e6b7b',
    tooltipShadow = 'rgba(0, 0, 0, 0.25)',
    gridLineColor = 'rgba(200, 200, 200, 0.2)',
    lineChartPrimary = '#ff9f43',
    lineChartDanger = '#666ee8',
    warningColorShade = '#ffe802'

    const { readyState } = wsCon()
  
  console.log("readyState", readyState)

  if ((readyState === 2) || (readyState === 3) || (readyState === null)) {
    wsDis()
    wsReCon()
    WsCheck()
  }

  if (readyState === 1) {
    WsCheck()
  }

  const chart_length = Object.keys(chart_data).length

  useEffect(() => {
    if (chart_length <= 0) {

      const start_date = format(addDays(new Date(), -7), "yyyy-MM-dd")
      const end_date = format(new Date(), "yyyy-MM-dd")

      axios.get('/display-config?config_type=dashboard_filter', { headers: { Authorization: token() } }).then(
        res => {
          if (res.data.message_type === "data_found") {
            let platformFinal = find_default_val(res.data.data[0].platform_val, platform)
            let severityFinal = find_default_val(res.data.data[0].severity_val, severity, true)

            if (platformFinal.values.length > 0 && severityFinal.values.length > 0) {              
              dispatch(dashboar_charts({ platform: platformFinal.values, threat_severity: severityFinal.values, start_date, end_date }))
              dispatch(dashboar_filter({ platform: platformFinal.labels, threat_severity: severityFinal.labels, defaultVals: {platformVal: platformFinal.defaultVals, severityVal : severityFinal.defaultVals, platformSetVal : platformFinal.values, severitySetVal: severityFinal.values }, start_date, end_date }))
            }
          }
        }
      )

    }

  }, [])
  
  return (
    <Fragment>
      <Breadcrumbs breadCrumbTitle={t('Dashboard')} />
      <Row className='match-height'>
        {/* Stats Card */}
        {/* <Col xl='6' md='6' xs='9'>
          <Threat_Detection_Type cols={{ xl: '4', sm: '8' }} />
        </Col> */}
        {/* Stats Card */}
        <Col lg='3' md='6' xs='12'>
          <Severity />
        </Col>
        <Col lg='3' md='6' xs='12'>
          <Leteral />
        </Col>
        <Col lg='3' md='6' xs='12'>
          <Internalattck />
        </Col>
        <Col lg='3' md='6' xs='12'>
          <External />
        </Col>
      </Row>
      <Row className='match-height'>
        <Col lg='8' md='6' xs='12'>
          <ThreatLogs />
        </Col>
        <Col lg='4' md='6' xs='12'>
          <Detectiontype />
        </Col>
      </Row>
      <Row className='match-height'>
        <Col lg='4' md='12' xs='12'>
          <Pie
            primary={context.colors.primary.main}
            warning={context.colors.warning.main}
            danger={context.colors.danger.main}
          />
        </Col>
        <Col lg='8' md='12' xs='12'>
          <Internal_vs_external
            warningColorShade={warningColorShade}
            lineChartDanger={lineChartDanger}
            lineChartPrimary={lineChartPrimary}
            labelColor={labelColor}
            tooltipShadow={tooltipShadow}
            gridLineColor={gridLineColor}
          />
        </Col>
      </Row>
       {/* <Col lg='12' sm='12'>
       <Newgraph />
       </Col> */}
    </Fragment>
  )
}

export default StatisticsCards
