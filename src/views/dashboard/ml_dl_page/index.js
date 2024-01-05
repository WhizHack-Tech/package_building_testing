// Filename : index.js
// Purpose/Description : This page representing the data of Ml & DL where IDS is not detecting. This is the index page of the folder where we import the different charts.  
// Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
// Copyright (c) : Whizhack Technologies (P) Ltd.

// Importing Component from verial folders of the project

import { useContext, useEffect, Fragment } from 'react'
import { ThemeColors } from '@src/utility/context/ThemeColors'
import Breadcrumbs from '@components/breadcrumbs/testpage'
import { useTranslation } from 'react-i18next'
import { test_page, test_filter } from "../../../redux/actions/charts/testpage"
import { useSelector, useDispatch } from "react-redux"
import { addDays, format } from "date-fns"
import { useRTL } from '@hooks/useRTL'
import { Row, Col } from 'reactstrap'
// Import CSS
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'
import '@styles/react/libs/tables/react-dataTable-component.scss'

//import cards
import Attacker_service from './Attacked__services'
import Total_attack_count from './Total_account_count'
import Internal_attack from './Internal_attack'
import CompromisedHost from './CompromisedHost'
import External_Attack from './External_Attack'
import ML_DL_Detection from './ML_DL_Detection'
import Table from './Table'
import ASN_Details from './ASN'
import Country_Chart from './Countrty'
import IP_Chart from './IP_Chart'
import City_Chart from './City'
import Attack_Frequency from './Attack_Frequency'
import axios from '@axios'
import { token } from '@utils'

const platform = [
  { value: 'aws', label: 'AWS', color: '#00B8D9', isFixed: true },
  { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
  { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
]

const accuracy = [
  { value: "1", label: "Between 91% to 100%" },
  { value: "2", label: "Between 76% to 90%" },
  { value: "3", label: "Between 65% to 75%" }
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
  // ** Hooks
  const {t} =  useTranslation()
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
  const chart_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(chart_data).length
  useEffect(() => {
    if (chart_length <= 0) {

      const start_date = format(addDays(new Date(), -7), "yyyy-MM-dd")
      const end_date = format(new Date(), "yyyy-MM-dd")

      axios.get('/display-config?config_type=dashboard_filter', { headers: { Authorization: token() } }).then(
        res => {
          if (res.data.message_type === "data_found") {
            let platformFinal = find_default_val(res.data.data[0].platform_val, platform)
            let accuracyFinal = find_default_val(`${res.data.data[0].accuracy_val}`, accuracy, true)

            if (platformFinal.values.length > 0) {
              dispatch(test_page({ platform: platformFinal.values, accuracy: accuracyFinal.values[0], start_date, end_date }))
              dispatch(test_filter({ platform: platformFinal.labels, accuracy: accuracyFinal.labels, defaultVals: {platformVal: platformFinal.defaultVals, accuracyVal : accuracyFinal.defaultVals, platformSetVal : platformFinal.values, accuracySetVal: accuracyFinal.values[0]}, start_date, end_date }))
            }
          }
        }
      )
    }

  }, [])

  return (
    <Fragment>
      <div className='ml-0'>
        <Breadcrumbs breadCrumbTitle={t("ML & DL Detection")} />
      </div>
      <Row className='match-height'>
        <Col md="4" xl="4">
          <Row>
            <Col md="12">
              <Attacker_service cols={{ md: '8', sm: '2' }} />
            </Col>
            <Col md='12'>
              <ML_DL_Detection cols={{ md: '8', sm: '2' }} />
            </Col>
          </Row>
        </Col>
        <Col md="8">
          <Row className='mx-0 match-height'>
            <Col md='3'>
              <Total_attack_count />
            </Col>
            <Col md='3'>
              <Internal_attack />
            </Col>
            <Col md='3'>
              <CompromisedHost />
            </Col>
            <Col md='3'>
              <External_Attack />
            </Col>
            <Col md='12' xs='12'>
              <Table />
            </Col>
          </Row>
        </Col>
        <Col md='12' xs='12'>
          <Row className='match-height' >
            <Col md="8">
              <Attack_Frequency primary={colors.primary.main} warning={colors.warning.main} />
              <ASN_Details
                successColorShade={successColorShade}
                labelColor={labelColor}
                tooltipShadow={tooltipShadow}
                gridLineColor={gridLineColor}
                lineChartPrimary={lineChartPrimary}
                yellowColor={yellowColor}
              />
            </Col>
            <Col md="4">
              <Country_Chart
                info={colors.info.main}
                labelColor={labelColor}
                tooltipShadow={tooltipShadow}
                gridLineColor={gridLineColor} />
              <City_Chart
                tooltipShadow={tooltipShadow}
                successColorShade={successColorShade}
                warningLightColor={warningLightColor}
                primary={colors.primary.main}
              />
            </Col>
          </Row >
        </Col>
        <Col lg='12' md='12' xs='12'>
          <IP_Chart direction={isRtl ? 'rtl' : 'ltr'}
            warning={colors.warning.main}
            primary={colors.primary.main}
            success={colors.success.main}
          />
        </Col>
      </Row>
    </Fragment>
  )
}
export default AttacksDashboard 
