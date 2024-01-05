import { useEffect, useState } from 'react'
import axios from 'axios'
import Chart from 'react-apexcharts'
import { Card, CardHeader, CardText, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'
const ActiveUsers = ({ success }) => {
    const [data, setData] = useState([])
  useEffect(() => {
    axios.get('http://localhost:3009/activeUsers').then((res) => {
      setData(res.data)
    })
  }, [])

  const options = {
    chart: {
      id: 'revenue',
      toolbar: {
        show: false
      },
      sparkline: {
        enabled: true
      }
    },
    grid: {
      show: false
    },
    colors: ['#90EE90'],
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth',
      width: 2.5
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 0.9,
        opacityFrom: 0.7,
        opacityTo: 0.5,
        stops: [0, 80, 100]
      }
    },

    xaxis: {
      labels: {
        show: false
      },
      axisBorder: {
        show: false
      }
    },
    yaxis: {
      labels: {
        show: false
      }
    },
    tooltip: {
      x: { show: true }
    }
  }
  const series = [
    {
      data: data.series
    }
  ]
  return (
    <Card>
    <CardHeader className='align-items-start pb-0'>
      <div>
        <h2 className='font-weight-bolder'>{data.total}</h2>
        <CardText>statTitle</CardText>
      </div>
      <span>
        <Button.Ripple color='primary' outline size='sm'>
          view More
        </Button.Ripple>
      </span>
    </CardHeader>
    <CardBody>
      <Chart options={options} series={series} type='area' />
    </CardBody>
  </Card>
  ) 
}

export default ActiveUsers
