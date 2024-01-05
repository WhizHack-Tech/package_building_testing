import axios from 'axios'
import { useState, useEffect } from 'react'
import Chart from 'react-apexcharts'
import { Link } from 'react-router-dom'
import { Info } from 'react-feather'
import { useTranslation } from 'react-i18next'
import { useSelector } from "react-redux"
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle, Badge, Popover, PopoverHeader, PopoverBody } from 'reactstrap'

const ApexLineChart = () => {
  const { t } = useTranslation()
  const areaColors = {
    series1: '#ffe700',
    series2: '#00d4bd',
    series3: '#826bf8',
    series4: '#2b9bf4',
    series5: '#FFA1A1',
    series6: '#008000',
    series7: '#f70d1a'
  }
  const chart_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(chart_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)

  let labelsData = [], series1Data = [], series2Data = [], series3Data = [], series4Data = [], series5Data = [], series6Data = [],
    series7Data = [], series1nameData = [], series2nameData = [], series3nameData = [], series4nameData = [], series5nameData = [],
    series6nameData = [], series7nameData = []

  if (chart_length > 0) {
    labelsData = chart_data.AttackerIPCount.labels
    series1Data = chart_data.AttackerIPCount.series1
    series2Data = chart_data.AttackerIPCount.series2
    series3Data = chart_data.AttackerIPCount.series3
    series4Data = chart_data.AttackerIPCount.series4
    series5Data = chart_data.AttackerIPCount.series5
    series6Data = chart_data.AttackerIPCount.series6
    series7Data = chart_data.AttackerIPCount.series7
    series1nameData = chart_data.AttackerIPCount.series1name
    series2nameData = chart_data.AttackerIPCount.series2name
    series3nameData = chart_data.AttackerIPCount.series3name
    series4nameData = chart_data.AttackerIPCount.series4name
    series5nameData = chart_data.AttackerIPCount.series5name
    series6nameData = chart_data.AttackerIPCount.series6name
    series7nameData = chart_data.AttackerIPCount.series7name
  }

  const options = {
    chart: {
      height: 350,
      type: 'line',
      zoom: {
        enabled: true
      },
      animations: {
        enabled: false
      }
    },
    stroke: {
      width: [5, 5, 4, 5, 4, 4, 4, 4, 4, 4],
      curve: 'straight'
    },
    labels: labelsData,
    colors: [areaColors.series1, areaColors.series2, areaColors.series3, areaColors.series4, areaColors.series5, areaColors.series6, areaColors.series7],
    xaxis: {
    }
  }

  const series = [
    {
      name: series1nameData,
      data: series1Data
    },
    {
      name: series2nameData,
      data: series2Data
    },
    {
      name: series3nameData,
      data: series3Data
    },
    {
      name: series4nameData,
      data: series4Data
    },
    {
      name: series5nameData,
      data: series5Data
    },
    {
      name: series6nameData,
      data: series6Data
    },
    {
      name: series7nameData,
      data: series7Data
    }

  ]

  return (
    <Card>
      <CardHeader className='d-flex flex-sm-row flex-column justify-content-md-between align-items-start justify-content-start'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Attacker IPs')}
          </CardTitle>
          {/* <CardSubtitle className='text-muted'>IP Attacks</CardSubtitle> */}
        </div>
        <Badge color='primary'>
          <Link><Info id='Attacker_IP' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Attacker_IP'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Attacker IPs')}</PopoverHeader>
          <PopoverBody>
            {t('Top Source IPs of the attackers')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <Chart options={options} series={series} type='line' height={300} />
      </CardBody>
    </Card>
  )
}

export default ApexLineChart
