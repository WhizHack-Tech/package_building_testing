import { Bar } from 'react-chartjs-2'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { Fragment, useState, useRef, useEffect } from 'react'
import { Info } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle, UncontrolledDropdown, UncontrolledButtonDropdown, Row, Button,
  DropdownToggle, Modal, ModalHeader, ModalBody, FormGroup, Input, CustomInput, ModalFooter,
  DropdownMenu, Spinner, Badge, Popover, PopoverHeader, PopoverBody,
  DropdownItem } from 'reactstrap'
  import axios from "axios"
  import { useSelector } from 'react-redux'

const ChartjsBarChart = ({ tooltipShadow, gridLineColor, labelColor, successColorShade, lineChartPrimary, yellowColor}) => {
  const {t} = useTranslation()
  const chart_data = useSelector((store) => store.attack_evnets_charts.charts)
  const chart_length = Object.keys(chart_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)
   
  let seriesData = [], labelsData = []
    if (chart_length > 0) {
      seriesData = chart_data.FrequentAttackerMackAddresses.series
      labelsData = chart_data.FrequentAttackerMackAddresses.labels
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
              labelString: 'MAC Address'
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
              // stepSize: 1000,
              // min: 0,
              // max: 400,
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
          {t('Attacker MAC Addresses')}</CardTitle>
        </div>
        <Badge color='primary'>
        <Link><Info id='Attacker_MAC_Addresses' size={20} /></Link>
      </Badge>
      <Popover
        placement='top'
        target='Attacker_MAC_Addresses'
        isOpen={popoverOpen}
        toggle={() => setPopoverOpen(!popoverOpen)}
      >
        <PopoverHeader>{t('Attacker MAC Addresses')}</PopoverHeader>
        <PopoverBody>
        {t('List of physical address of most frequent attackers of your network Top Source MAC Addresses of the attackers')}
        </PopoverBody>
      </Popover>
      </CardHeader>
      <CardBody>
        <div style={{ height: '350px' }}>
          <Bar data={data} options={options} height={320} />
        </div>
      </CardBody>
     
    </Card>
  )
}

export default ChartjsBarChart
