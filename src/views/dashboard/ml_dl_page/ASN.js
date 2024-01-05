import { Bar } from 'react-chartjs-2'
import { useTranslation } from 'react-i18next'
import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle, Spinner, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { Link } from 'react-router-dom'
import { Info } from 'react-feather'
import { useSelector } from "react-redux"

const ChartjsBarChart = ({ tooltipShadow, gridLineColor, labelColor, successColorShade, lineChartPrimary, yellowColor }) => {
  const { t } = useTranslation()
  const chart_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(chart_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)

  let seriesData = [], labelsData = []
  if (chart_length > 0) {
    seriesData = chart_data.AsnNameCount.series
    labelsData = chart_data.AsnNameCount.labels
  }

  const options = {
    elements: {
      rectangle: {
        borderWidth: 2,
        borderSkipped: 'bottom'
      }
    },
    responsive: true,
    maintainAspectRatio: false,
    responsiveAnimationDuration: 500,
    legend: {
      display: false
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
    scales: {
      xAxes: [
        {
          display: true,
          gridLines: {
            display: true,
            color: gridLineColor,
            zeroLineColor: gridLineColor
          },
          scaleLabel: {
            display: true,
            labelString: 'ASN'
          },
          ticks: {
            fontColor: labelColor
          }
        }
      ],
      yAxes: [
        {
          display: true,
          gridLines: {
            color: gridLineColor,
            zeroLineColor: gridLineColor
          },
          scaleLabel: {
            display: true,
            labelString: 'Count'
          },
          ticks: {
            //stepSize: 1000,
            //  min: 0,
            // max: 400
            fontColor: labelColor
          }
        }
      ]
    }
  },
    data = {
      // labels: ['Routers', 'Laptops', 'Phones', 'Subnet', 'Servers', 'Dummy', 'Dummy'],
      labels: labelsData,
      datasets: [
        {
          data: seriesData,
          backgroundColor: lineChartPrimary,
          borderColor: 'transparent',
          barThickness: 35
        }
      ]
    }


  return (
    <Card>
      <CardHeader className='d-flex justify-content-between align-items-sm-center align-items-start flex-sm-row flex-column'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Top Attacker ASNs')}
          </CardTitle>
        </div>
        <Badge color='primary'>
          <Link><Info id='Attacker_ASN' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Attacker_ASN'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Top Attacker ASNs')}</PopoverHeader>
          <PopoverBody>
            {t('Line chart represents the top Autonomous System Number used by the attacker detected by the Geo-Location detection system')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <div style={{ height: '400px' }}>
          <Bar data={data} options={options} height={400} />
        </div>
      </CardBody>

    </Card>
  )
}

export default ChartjsBarChart
