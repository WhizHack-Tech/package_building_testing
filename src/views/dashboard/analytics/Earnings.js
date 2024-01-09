import axios from '@axios'
import { useEffect, useState } from 'react'
import Chart from 'react-apexcharts'
import { Card, CardTitle, CardText, CardBody, Row, Col } from 'reactstrap'

const Earnings = ({ success }) => {

  const [month_earningdata, setMonth_earningData] = useState([])
  const [last_monthdata, setLast_monthData] = useState([])
  const [seriesdata, setSeriesData] = useState([])
  const [averagedata, setAverageData] = useState([])


  useEffect(() => {
    axios.get('/earnings').then((res) => {
     setMonth_earningData(res.data.month_earning)
     setLast_monthData(res.data.last_month)
     setSeriesData(res.data.series)
     setAverageData(res.data.average)
    })
  }, [])
  const options = {
    chart: {
      toolbar: {
        show: false
      }
    },
    dataLabels: {
      enabled: false
    },
    legend: { show: false },
    comparedResult: [2, -3, 8],
    labels: ['Silver', 'Diamond', 'Gold'],
    stroke: { width: 0 },
    //colors: ['#28c76f66', '#28c76f33', success],
    grid: {
      padding: {
        right: -20,
        bottom: -8,
        left: -20
      }
    },
    plotOptions: {
      pie: {
        startAngle: -10,
        donut: {
          labels: {
            show: true,
            name: {
              offsetY: 15
            },
            value: {
              offsetY: -15,
              formatter(val) {
                return `${parseInt(val)} %`
              }
            },
            total: {
              show: true,
              offsetY: 15,
              label: 'App',
              formatter(w) {
                return '34'
              }
            }
          }
        }
      }
    },
    responsive: [
      {
        breakpoint: 1325,
        options: {
          chart: {
            height: 100
          }
        }
      },
      {
        breakpoint: 1200,
        options: {
          chart: {
            height: 120
          }
        }
      },
      {
        breakpoint: 1065,
        options: {
          chart: {
            height: 100
          }
        }
      },
      {
        breakpoint: 992,
        options: {
          chart: {
            height: 120
          }
        }
      }
    ]
  }
  // const series = [seriesdata]
  return (
    <Card className='earnings-card'>
      <CardBody>
        <Row>
          <Col xs='6'>
            <CardTitle className='mb-1'>Earnings</CardTitle>
            <div className='font-small-2'>This Month</div>
            <h5 className='mb-1'>{month_earningdata}</h5>
            <CardText className='text-muted font-small-2'>
              <span className='font-weight-bolder'>{last_monthdata}</span>
              <span> more earnings than last month.</span>
            </CardText>
          </Col>
          <Col xs='6'>
            <Chart options={options} series={[20, 30, 40]} type='donut' height={120} />
          </Col>
        </Row>
      </CardBody>
    </Card>
  )
}

export default Earnings
