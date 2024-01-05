    // Filename : Pie.js
    // Purpose/Description : This is a pie chart which is representing the attacks in the environment based on Internal Attacks and External Attacks
    // Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
    // Copyright (c) : Whizhack Technologies (P) Ltd.
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
// import { FormattedMessage } from 'react-intl'
import { useTranslation } from 'react-i18next'
import Botnet from "../../../assets/images/svg/internal_copy.svg"
import external from "../../../assets/images/svg/external_copy.svg"
import internal from "../../../assets/images/svg/Critical_copy.svg"
import {
  Card,
  CardHeader,
  CardTitle,
  CardBody, Popover, PopoverHeader, PopoverBody, Badge
} from 'reactstrap'
// import * as Icon from 'react-feather'
import { Sunrise, Info, Sunset } from 'react-feather'
//importing apexchart
import Chart from 'react-apexcharts'
import { useSelector } from "react-redux"
const PieChart = props => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)

  const charts_data = useSelector((store) => store.dashboard_charts.charts)

  const chart_length = Object.keys(charts_data).length

  //Chart edit option starts from here
  const options = {
    chart: {
      toolbar: {
        show: true
      }
    },
    labels: ['Internal Attacks', 'Outgoing Botnet Connections', 'External Attacks'],
    dataLabels: {
      enabled: true
    },
    legend: { show: false },
    stroke: {
      width: 4
    },
    colors: [props.danger, props.primary, props.warning]
  }

  return (
    <Card>
      <CardHeader className='align-items-end'>
            <CardTitle tag='h4'>{t('Overall Attack Comparison')}</CardTitle>
                <Badge color='primary'>
                  <Link><Info id='Overall_Attack_Comparison' size={20} /></Link>
                </Badge>
            <Popover
                  placement='top'
                  target='Overall_Attack_Comparison'
                  isOpen={popoverOpen}
                  toggle={() => setPopoverOpen(!popoverOpen)}
                >
                    <PopoverHeader>{t('Overall Attack Comparison')}</PopoverHeader>
                      <PopoverBody>
                        {t('We represent here attacks in the environment based on Internal Attacks and External Attacks')}
                      </PopoverBody>
            </Popover>
          </CardHeader>
      <CardBody>
      <div style={{ height: '480px' }}>
         <Chart options={options} series={(chart_length > 0) ? charts_data.internal_external_pie_chart.series : []} type='pie' height={300} />
      
                <div className='d-flex justify-content-between mt-0 mb-0'>
                  <div className='d-flex align-items-center'>
                  <img width={40} src={internal} />
                    {/* <Sunset size={17} className='text-primary' /> */}
                    <span className='font-weight-bold ml-55 mr-20'>{t('Outgoing Botnet Connections')}</span>
                  </div>
                  <div>
                    <span>{(chart_length > 0) ? charts_data.internal_external_pie_chart.internal_compromised_machine_count : ""}</span>
                  </div>
                </div>
                <div className='d-flex justify-content-between mt-1 mb-1'>
                  <div className='d-flex align-items-center'>
                  <img width={40} src={external} />
                    {/* <Sunrise size={17} className='text-warning' /> */}
                    <span className='font-weight-bold ml-55 mr-20'>{t('External Attacks')}</span>
                  </div>
                  <div>
                    <span>{(chart_length > 0) ? charts_data.internal_external_pie_chart.external_count : ""}</span>
                  </div>
                </div>
                <div className='d-flex justify-content-between mt-1 mb-1'>
                  <div className='d-flex align-items-center'>
                    {/* <Info size={17} className='text-danger' /> */}
                    <img width={40} src={Botnet} />
                    <span className='font-weight-bold ml-55 mr-20'>{t('Internal Attacks')}</span>
                    </div>
                    <div>
                  <span>{(chart_length > 0) ? charts_data.internal_external_pie_chart.lateral_mov_count : ""}</span>
                </div>
                </div>
      </div>          
      </CardBody>
    </Card>
  )
}
export default PieChart
