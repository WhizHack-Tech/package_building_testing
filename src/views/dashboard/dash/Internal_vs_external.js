    // Filename : Internal_vs_external.js
    // Purpose/Description : This file having the code of internal vs external attack line chart. 
    // Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
    // Copyright (c) : Whizhack Technologies (P) Ltd.
// Importing Component from verial folders of the project
import { useState, useEffect } from 'react'
//import the apexchart
import Chart from 'react-apexcharts'
import { Link } from 'react-router-dom'
import { Info } from 'react-feather'
import { useSelector } from "react-redux"
//import react-intl library for language change
// import { FormattedMessage } from 'react-intl'
import { useTranslation } from 'react-i18next'
//imort css of the table
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
//Define the colour of the line charts
const areaColors = {
  series3:'#666ee8',
  series2:'#ff9f43',
  series1:'#ff5343'
}
const ChartjsLineChart = ({direction, warning}) => {
  const {t} = useTranslation()
  const charts_data = useSelector((store) => store.dashboard_charts.charts)
  const chart_length = Object.keys(charts_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)

  let internal = [], external = [], lateral = [], labels = []
  if (chart_length > 0) {
    internal = charts_data.internal_external_count.internal_compromised_machine
    external = charts_data.internal_external_count.external
    lateral = charts_data.internal_external_count.lateral_movement
    labels = charts_data.internal_external_count.labels
  }
//chart modification section
  const options = {
    chart: {
      zoom: {
        enabled: true
      },
      parentHeightOffset: 0,
      toolbar: {
        show: true
      }
    },
    // markers: {
    //   strokeWidth: 7,
    //   strokeOpacity: 1,
    //   strokeColors: ['#fff'],
    //   colors: [warning]
    // },
    dataLabels: {
      enabled: false
    },
    stroke: {
      show: true,
      curve: 'smooth'
    },
    legend: {
      position: 'top',
      horizontalAlign: 'start'
    },
  grid: {
      xaxis: {
        lines: {
          show: true
        }
      },
      yaxis: {
        lines: {
          show: false
        }
      }
    },
    colors: [areaColors.series3, areaColors.series2, areaColors.series1],
    xaxis: {
      categories: labels,
      scaleLabel: {
        display: true,
        labelString: 'Dates'
      }
    },
    tooltip: {
      shared: true
    },
    yaxis: {
      opposite: direction === 'rtl'
    }
  }

//name of the charts define here
  const series = [
    {
      name: t('Outgoing Botnet Connections'),
      data: internal
    },
    {
      name: t('External Attacks'),
      data: external
    },
{
      name: t('Internal Attacks'),
      data: lateral
    }
  ]
  return (
    <Card>
      <CardHeader className='d-flex justify-content-between align-items-sm-center align-items-start flex-sm-row flex-column'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
          {t('Internal and External Attack Comparison')}
          </CardTitle>
        </div>
        <Badge color='primary'>
          <Link><Info id='Internal_VS_External_Attack' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Internal_VS_External_Attack'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Internal and External Attack Comparison')}</PopoverHeader>
          <PopoverBody>
          {t('Line chart representing comparison between Internal and External Attacks')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <div style={{ height: '480px' }}>
          <Chart options={options} series={series} type='area' height={480} />
        </div>
      </CardBody>
    </Card>
  )
}

export default ChartjsLineChart