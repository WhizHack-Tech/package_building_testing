import { useTranslation } from 'react-i18next'
import { HorizontalBar } from 'react-chartjs-2'
import { Link } from 'react-router-dom'
import { Info} from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle, Spinner, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { Fragment, useState, useRef, useEffect } from 'react'
import { useSelector } from "react-redux"

const ChartjsHorizontalBarChart = ({ tooltipShadow, gridLineColor, labelColor, info }) => {
  const {t} = useTranslation()
  const chart_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(chart_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)

   let seriesData = [], labelsData = []
   
    if (chart_length > 0) {
      seriesData = chart_data.GeoipCountryCount.series
      labelsData = chart_data.GeoipCountryCount.labels
    }
   
  const donutColors = {
    series1: '#ffe700',
    series2: '#00d4bd',
    series3: '#826bf8',
    series4: '#2b9bf4',
    series5: '#FFA1A1',
    series6: '#008000',
    series7: '#242926'
  }

  const options = {
      elements: {
        rectangle: {
          borderWidth: 2,
          borderSkipped: 'left',
          borderSkipped: 'top'
        }
      },
      tooltips: {
        // Updated default tooltip UI
        shadowOffsetX: 1,
        shadowOffsetY: 1,
        shadowBlur: 8,
        shadowColor: tooltipShadow,
        backgroundColor: '#fff',
        titleFontColor: '#000',
        bodyFontColor: '#000'
      },
      responsive: true,
      maintainAspectRatio: false,
      responsiveAnimationDuration: 500,
      legend: {
        display: false
      },
      layout: {
        padding: {
          bottom: -30,
          left: -25
        }
      },
      scales: {
        xAxes: [
          {
            display: true,
            gridLines: {
              zeroLineColor: gridLineColor,
              borderColor: 'transparent',
              color: gridLineColor,
              drawTicks: false
            },
            scaleLabel: {
              display: true
            },
            ticks: {
              min: 0,
              fontColor: labelColor
            }
          }
        ],
        yAxes: [
          {
            display: true,
            gridLines: {
              display: false
            },
            scaleLabel: {
              display: true
            },
            ticks: {
              fontColor: labelColor
            }
          }
        ]
      }
    },
    data = {
      // labels: ['Washington DC', 'Lonsdsdon', 'New York', 'Delhi', 'Hong Kong', 'Shanghai', 'New Jersey'],
      labels: labelsData,
      datasets: [
        {
          data: seriesData,
          backgroundColor: '#826bf8',
          borderColor: 'transparent',
          barThickness: 35
        }
      ]
    }

  return (
    <Card>
    <CardHeader>
      <div>
        <CardTitle className='mb-75' tag='h4'>
        {t('Top Source Attack Countries')}
        </CardTitle>
        </div>
        <Badge color='primary'>
        <Link><Info id='Source_Attack_Countries' size={20} /></Link>
      </Badge>
      <Popover
        placement='top'
        target='Source_Attack_Countries'
        isOpen={popoverOpen}
        toggle={() => setPopoverOpen(!popoverOpen)}
      >
        <PopoverHeader>{t('Top Source Attack Countries')}</PopoverHeader>
        <PopoverBody>
        {t('Top Countries from where attack originates')}
        </PopoverBody>
      </Popover>
    </CardHeader>
      <CardBody>
        <div style={{ height: '300px'}}>
          <HorizontalBar data={data} options={options} height={300} />
        </div>
      </CardBody>
    </Card>
  )
}

export default ChartjsHorizontalBarChart
