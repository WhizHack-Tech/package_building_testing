import Chart from 'react-apexcharts'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Info } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle, Row, Badge, Spinner, Popover, PopoverHeader, PopoverBody } from 'reactstrap'
import { useSelector } from "react-redux"

const ApexLineChart = ({ direction, warning }) => {
  const { t } = useTranslation()
  const chart_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(chart_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)

  let seriesData = [], categoriesData = []
  if (chart_length > 0) {
    seriesData = chart_data.FrequencyOfAttacks.series
    categoriesData = chart_data.FrequencyOfAttacks.categories
  }

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
    dataLabels: {
      enabled: false
    },
    stroke: {
      show: true,
      curve: 'smooth'
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
    tooltip: {
      custom(data) {
        return `<div class='px-1 py-50'>
              <span>${data.series[data.seriesIndex][data.dataPointIndex]}</span>
            </div>`
      }
    },
    xaxis: {
      categories: categoriesData,
      scaleLabel: {
        display: true,
        labelString: 'Dates'
      }
    },
    yaxis: {
      opposite: direction === 'rtl'
    }
  }

  const series = [
    {
      data: seriesData
    }
  ]
  return (
    <Card>
      <CardHeader className='d-flex flex-sm-row flex-column justify-content-md-between align-items-start justify-content-start'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Attack Frequency')}
          </CardTitle>
        </div>
        <Badge color='primary'>
          <Link><Info id='Frequency_of_Attacks' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Frequency_of_Attacks'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Attack Frequency')}</PopoverHeader>
          <PopoverBody>
            {t('Line chart represents the frequency of attacks detected by the Triple Layered Detection Engine')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <Chart options={options} series={series} type='area' height={200} />
      </CardBody>

    </Card>
  )
}

export default ApexLineChart
