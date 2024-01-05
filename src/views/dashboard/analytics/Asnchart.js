// Filename : top_attacks_doughnutcharts.js

// Purpose/Description : This charts representing top attacks in the enviroment and collect the data from database which is attack_threat_class and showing the data using grouby query

// Author : Jaydeep Roy Sarkar and Sai Kaladhar

// Copyright (c) : Whizhack Technologies (P) Ltd.

import Chart from 'react-apexcharts'
import { Link } from 'react-router-dom'
import { useState } from 'react'

import { useTranslation } from 'react-i18next'
import { Info } from 'react-feather'
import {
  Card, CardHeader, CardTitle, CardBody, CardSubtitle,
  Popover, PopoverHeader, PopoverBody, Badge, Spinner
} from 'reactstrap'
import { useSelector } from 'react-redux'
import "../chart-style.css"

const SpinnerColors = () => {
  const { t } = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const chart_data = useSelector((store) => store.attack_evnets_charts.charts)
  const chart_length = Object.keys(chart_data).length
  // const [labelsData, setLabelsData] = useState([])
  // const [seriesData, setSeriesData] = useState([])  
  let labelsData = [], seriesData = []

  if (chart_length > 0) {
    seriesData = chart_data.TcpCount.series
    labelsData = chart_data.TcpCount.labels
  }

  const donutColors = {
    series1: '#826bf8',
    series2: '#00d4bd',
    series3: '#ffe700',
    series4: '#2b9bf4',
    series5: '#FFA1A1',
    series6: '#008000',
    series7: '#f70d1a',
    series8: '#a80d1d',
    series9: '#0db8a1',
    series10: '#851410',
    series11: '#81d40d',
    series12: '#ee00ff',
    series13: '#826bf8',
    series14: '#2b9bf4',
    series15: '#FFA1A1',
    series16: '#008000',
    series17: '#242926',
    series18: '#242926'
  }
  const options = {
    chart: {
      id: 112233,
      zoom: {
        enabled: true
      },
      parentHeightOffset: 0,
      toolbar: {
        show: true
      }
    },
    legend: {
      show: true,
      position: 'bottom',
      fontFamily: 'Helvetica, Arial',
      onItemClick: {
        toggleDataSeries: true
      },
      onItemHover: {
        highlightDataSeries: true
      }
    },
    labels: labelsData,
    colors: [donutColors.series1, donutColors.series2, donutColors.series3, donutColors.series4, donutColors.series5, donutColors.series6, donutColors.series7, donutColors.series8, donutColors.series9, donutColors.series10, donutColors.series11, donutColors.series12, donutColors.series13, donutColors.series14, donutColors.series15, donutColors.series16, donutColors.series17, donutColors.series18],
    dataLabels: {
      enabled: true,
      formatter(val, opt) {
        return `${parseInt(val)}%`
      }
    },
    plotOptions: {
      pie: {
        donut: {
          labels: {
            show: false,
            name: {
              fontSize: '1rem',
              fontFamily: 'Montserrat'
            },
            value: {
              fontSize: '1.9rem',
              fontFamily: 'Montserrat',
              formatter(val) {
                return `${parseInt(val)}`
              }
            },
            total: {
              show: true,
              fontSize: '1.9rem',
              labels: labelsData[0],
              formatter(w) {
                return `${seriesData[0]}`
              }
            }
          }
        }
      }
    }
  }
  const series = seriesData

  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Most Attacked Ports')}
          </CardTitle>
        </div>
        <Badge color='primary'>
          <Link><Info id='Attacker_Ports' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Attacker_Ports'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Most Attacked Ports')}</PopoverHeader>
          <PopoverBody>
            {t('Top destination ports targeted by Attackers')}</PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <Chart options={options} series={series} type='donut' height={320} />
      </CardBody>
    </Card>
  )
}

export default SpinnerColors