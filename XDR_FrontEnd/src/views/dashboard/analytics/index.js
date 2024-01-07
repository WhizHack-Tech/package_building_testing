// Filename : top_attacks_doughnutcharts.js
// Purpose/Description : This page collecting data from dashboard folder and showing in the page after importing the pages 
// Author : Jaydeep Roy Sarkar and Sai Kaladhar
// Copyright (c) : Whizhack Technologies (P) Ltd.

// Importing Component from verial folders of the project

import { useContext, useEffect } from 'react'
import { ThemeColors } from '@src/utility/context/ThemeColors'
import Breadcrumbs from '@components/breadcrumbs/attack-events'
import { useTranslation } from 'react-i18next'
import { Row, Col } from 'reactstrap'
import MacAddress from './MacAddress'
import Top_attack_countries from './Top_attack_countries_Doughnutchart'
import ApexLineChart from './ApexLineChart'
import MAP from './Map'
import Attackcounts from './Attackcounts'
import Asnchart from './Asnchart'
import IP_Line_chart from './IP_Line_chart'
import Citypie from './Citypie'
import ASN_Details from './ASN_Details'
import { useRTL } from '@hooks/useRTL'
import { attack_events_charts, attack_filter } from "../../../redux/actions/charts/attack-events-actions"
import { useSelector, useDispatch } from "react-redux"
import { addDays, format } from "date-fns"
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'
import axios from '@axios'
import { token } from '@utils'

const platform = [
  { value: 'aws', label: 'AWS', color: '#00B8D9', isFixed: true },
  { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
  { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
]

const severity = [
  { value: '1', label: 'High', color: '#00B8D9' },
  { value: '2', label: 'Medium', color: '#0052CC' },
  { value: '3', label: 'Low', color: '#5243AA' }
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

const AttacksDashboard = () => {
  const {t} = useTranslation()
  // ** Hooks
  const [isRtl, setIsRtl] = useRTL()
  const { colors } = useContext(ThemeColors),
    labelColor = 'dark' ? '#b4b7bd' : '#6e6b7b',
    tooltipShadow = 'rgba(0, 0, 0, 0.25)',
    gridLineColor = 'rgba(200, 200, 200, 0.2)',
    lineChartPrimary = '#666ee8',
    lineChartDanger = '#ff4961',
    warningColorShade = '#ffe802',
    warningLightColor = '#FDAC34',
    successColorShade = '#28dac6',
    yellowColor = '#ffe800'
  const dispatch = useDispatch()
  const chart_data = useSelector((store) => store.attack_evnets_charts.charts)
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
              dispatch(attack_events_charts({ platform: platformFinal.values, threat_severity: severityFinal.values, start_date, end_date }))
              dispatch(attack_filter({ platform: platformFinal.labels, threat_severity: severityFinal.labels, defaultVals: {platformVal: platformFinal.defaultVals, severityVal : severityFinal.defaultVals, platformSetVal : platformFinal.values, severitySetVal: severityFinal.values }, start_date, end_date }))
            }
          }
        }
      )
    }

  }, [])


  return (
    <div id='dashboard-analytics'>
      <Breadcrumbs breadCrumbTitle={t("Attack Events")} />
      <Row>
        <Col lg='12' md='12' xs='12'>
          <Attackcounts cols={{ md: '2', sm: '4' }} />
        </Col>
      </Row>
      <Row className='match-height'>
        <Col lg='6' md='12' xs='12'>
          <Top_attack_countries
            info={colors.info.main}
            labelColor={labelColor}
            tooltipShadow={tooltipShadow}
            gridLineColor={gridLineColor} />
        </Col>
        <Col lg='6' md='12' xs='12'>
          <MAP />
        </Col>
      </Row>
      <Row className='match-height'>
        <Col lg='4' md='12' xs='12'>
          <Citypie
            tooltipShadow={tooltipShadow}
            successColorShade={successColorShade}
            warningLightColor={warningLightColor}
            primary={colors.primary.main}
          />
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
          <IP_Line_chart direction={isRtl ? 'rtl' : 'ltr'}
            warning={colors.warning.main}
            primary={colors.primary.main}
            success={colors.success.main}
          />
        </Col>
        <Col lg='4' md='12' xs='12'>
          <Asnchart
            tooltipShadow={tooltipShadow}
            successColorShade={successColorShade}
            warningLightColor={warningLightColor}
            primary={colors.primary.main}
          />
        </Col>
      </Row>
      <Row className='match-height'>
        <Col lg='6' md='12' xs='12'>
          <MacAddress
            warningColorShade={warningColorShade}
            lineChartDanger={lineChartDanger}
            lineChartPrimary={lineChartPrimary}
            labelColor={labelColor}
            tooltipShadow={tooltipShadow}
            gridLineColor={gridLineColor}
          />
        </Col>
        <Col lg='6' md='12' xs='12'>
          <ApexLineChart primary={colors.primary.main} warning={colors.warning.main} />
        </Col>
      </Row>
    </div>
  )
}

export default AttacksDashboard
