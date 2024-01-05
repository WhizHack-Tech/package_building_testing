// ** Third Party Components
import Chart from 'react-apexcharts'
import { useEffect, useState } from 'react'
import axios from '@axios'
import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import PreLoader from '../preLoader'
import { token } from '@utils'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { Card, CardHeader, CardText, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Row, Col, CardTitle } from 'reactstrap'

const Earnings = ({ success }) => {
  const [internal, setInternal] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart)
  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`nids-alert-int-compr?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)
        if (res.data.message_type === "success") {
          setInternal(res.data)
        }
      })
      .catch(error => {
        setApiLoader(false)
        console.log(error.message)
      })


  }

  useEffect(() => {
    apiLogic()

  }, [filterState.values, filterState.refreshCount])

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
    labels: ['External', 'Internal', 'Lateral'],
    stroke: { width: 0 },
    colors: ['#28c76f66', '#28c76f33', success],
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
                return `${parseInt(val)} `
              }
            },
            total: {
              show: true,
              offsetY: 15,
              // label: 'App',
              formatter() {
                return ''
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

  return (
    <Card className='earnings-card'>
      <CardBody>
      <div style={{ height: '120px' }}>
        <Row>
          <Col xs='6'>
            <CardTitle className='mb-1'>Type of Threat</CardTitle>
            <div className='font-small-2'>Total Threat Count</div>
            <h5 className='mb-1'>4055</h5>
          </Col>
          <Col xs='6'>
            <Chart options={options} series={[49, 26, 27]} type='donut' height={120} />
          </Col>
        </Row>
        </div>
      </CardBody>
      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default Earnings
