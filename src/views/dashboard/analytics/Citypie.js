import Chart from 'react-apexcharts'
import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { Info } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle, Spinner, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { useSelector } from "react-redux"
import "../chart-style.css"

const ApexRadiarChart = () => {
  const { t } = useTranslation()
  const chart_data = useSelector((store) => store.attack_evnets_charts.charts)
  const chart_length = Object.keys(chart_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)

  let labelsData = [], seriesData = []
  if (chart_length > 0) {
    seriesData = chart_data.Geoipcityname.series
    labelsData = chart_data.Geoipcityname.labels
  }

  const donutColors = {
    series1: '#826bf8',
    series2: '#21409F',
    series3: '#01a14b',
    series4: '#3EB489',
    series5: '#F70D1A',
    series6: '#2916F5',
    series7: '#F0E68C',
    series8: '#EDDA74',
    series9: '#FFD801',
    series10: '#F4A460',
    series11: '#C2B280',
    series12: '#C04000',
    series13: '#FF6347'
  }
  const options = {
    chart: {
      id: 223344,
      zoom: {
        enabled: false
      },
      parentHeightOffset: 0,
      toolbar: {
        show: true
      }
    },
    legend: {
      show: true,
      position: 'bottom',
      horizontalAlign: 'center',
      markers: {
        width: 10,
        height: 10
      }
    },
    labels: labelsData,
    colors: [donutColors.series1, donutColors.series2, donutColors.series3, donutColors.series4, donutColors.series5, donutColors.series6, donutColors.series7, donutColors.series8, donutColors.series9, donutColors.series10, donutColors.series11, donutColors.series12, donutColors.series13],
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

  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Top Attacker Cities')}
          </CardTitle>
        </div>
        <Badge color='primary'>
          <Link><Info id='Attacker_City' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Attacker_City'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader> {t('Top Attacker Cities')}</PopoverHeader>
          <PopoverBody>
            {t('Top Cities from where the attacks originate')}</PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <Chart options={options} series={seriesData} type='pie' height={310} />
      </CardBody>
    </Card>
  )
}

export default ApexRadiarChart
