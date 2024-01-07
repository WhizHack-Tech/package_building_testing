// Importing Component from verial folders of the project
import { Row, Col } from 'reactstrap'
import Breadcrumbs from '@components/breadcrumbs/tables_chart'
import { useTranslation } from 'react-i18next'
// Import CSS
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/base/pages/dashboard-ecommerce.scss'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import Top_Victim from './Top_Victim'
import Top_Attacking from './Top_Attacking'
import Fastest_Attackers from './Fastest_Attackers'
import Geo from './Geo'
import Top_Attack from './Top_Attack'
import Attack_Types from './Attack_Types'
import { tables_charts, table_filter } from "../../../redux/actions/charts/tables_charts"
import { useSelector, useDispatch } from "react-redux"
import { useEffect } from 'react'
import { addDays, format } from "date-fns"
import '@styles/react/libs/tables/react-dataTable-component.scss'
import axios from '@axios'
import { token } from '@utils'

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

const EcommerceDashboard = () => {
  const {t} = useTranslation()
  const dispatch = useDispatch()
  const chart_data = useSelector((store) => store.tables_charts.charts)
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
              dispatch(tables_charts({ platform: platformFinal.values, threat_severity: severityFinal.values, start_date, end_date }))              
              dispatch(table_filter({ platform: platformFinal.labels, threat_severity: severityFinal.labels, defaultVals: {platformVal: platformFinal.defaultVals, severityVal : severityFinal.defaultVals, platformSetVal : platformFinal.values, severitySetVal: severityFinal.values }, start_date, end_date }))
            }
          }
        }
      )
    }

  }, [])

  return (
    <div id='dashboard-ecommerce'>

      <Breadcrumbs breadCrumbTitle={t('Intelligence')} />
      <Row className='match-height'>
        <Col lg='6' md='12' xs='12'>
          <Top_Victim />
        </Col>
        <Col lg='6' md='12' xs='12'>
          <Top_Attacking />
        </Col>
      </Row>
      <Row className='match-height'>
        <Col lg='6' md='12' xs='12'>
          <Fastest_Attackers />
        </Col>
        <Col lg='6' md='12' xs='12'>
          <Geo />
        </Col>
      </Row>
      <Row className='match-height'>
        {/* <Col lg='6' md='6' xs='6'>
        <Tcp_service />
        </Col>  */}
        {/* <Col lg='6' md='6' xs='6'>
        <Udp_services />
        </Col>  */}
      </Row>
      <Row className='match-height'>
        <Col lg='6' md='12' xs='12'>
          <Top_Attack />
        </Col>
        <Col lg='6' md='12' xs='12'>
          <Attack_Types />
        </Col>
      </Row>
    </div>
  )
}

export default EcommerceDashboard
