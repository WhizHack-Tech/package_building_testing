
import Chart from 'react-apexcharts'
import { useEffect, useState } from 'react'
import { Settings } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText } from 'reactstrap'

//Import ThirdParty Application
import axios from 'axios'
import { kFormatter } from '@utils'
import { formatRange } from '@fullcalendar/core'
import { setLocale } from 'yup'

const Sales2 = props => {
  // const [data, setData] = useState(null)

  //   useEffect(() => {
  //     axios.get('/card/card-analytics/sales').then(res => setData(res.data))
  //   }, [])
    const [seriesdata, setSeriesData] = useState([])
    const [labelsdata, setlablesData] = useState([])
    const [yearsdata, setYearsData] = useState([])
    const [totaldata, setTotalData] = useState([])

    useEffect(() => {
      axios.get('http://127.0.0.1:8000/sales').then((res) => {
        setSeriesData(res.data.series)
        setlablesData(res.data.lables)
        setYearsData(res.data.years)
        setTotalData(res.data.total)
      })
    }, [])

  const options = {
      chart: {
        toolbar: { show: false },
        zoom: { enabled: false },
        type: 'line',
        dropShadow: {
          enabled: true,
          top: 18,
          left: 2,
          blur: 5,
          opacity: 0.2
        },
        offsetX: -10
      },
      stroke: {
        curve: 'smooth',
        width: 4
      },
      grid: {
        borderColor: '#ebe9f1',
        padding: {
          top: -20,
          bottom: 5,
          left: 20
        }
      },
      legend: {
        show: true
      },
      colors: ['#df87f2'],
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          inverseColors: false,
          gradientToColors: [props.primary],
          shadeIntensity: 1,
          type: 'horizontal',
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100, 100, 100]
        }
      },
      markers: {
        size: 0,
        hover: {
          size: 5
        }
      },
      xaxis: {
        labels: {
          offsetY: 5,
          style: {
            colors: '#b9b9c3',
            fontSize: '0.857rem',
            fontFamily: 'Montserrat'
          }
        },
        axisTicks: {
          show: false
        },
        categories: labelsdata,
        axisBorder: {
          show: false
        },
        tickPlacement: 'on'
      },
      yaxis: {
        tickAmount: 5,
        labels: {
          style: {
            colors: '#b9b9c3',
            fontSize: '0.857rem',
            fontFamily: 'Montserrat'
          },
          formatter(val) {
            return val > 999 ? `${(val / 1000).toFixed(1)}k` : val
          }
        }
      },
      tooltip: {
        x: { show: false }
      }
    },
    series = [
      {
        name: 'Sales',
        data: seriesdata
      }
    ]
  return (
    <Card>
      <CardHeader className='align-items-start'>
        <div>
          <CardTitle className='mb-25' tag='h4'>
            Sales
          </CardTitle>
          <CardText className='mb-0'>{yearsdata} Total Sales: {kFormatter(totaldata)}</CardText>
        </div>
        {/* <Settings size={18} className='text-muted cursor-pointer' /> */}
      </CardHeader>
      <CardBody className='pb-0'>
        <Chart options={options} series={series} type='line' height={240} />
      </CardBody>
    </Card>
  )
}
export default Sales2
