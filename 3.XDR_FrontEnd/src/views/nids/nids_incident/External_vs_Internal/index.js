import Chart from 'react-apexcharts'
import { useEffect, useState } from 'react'
import axios from '@axios'
import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import PreLoader from '../preLoader'
import { token } from '@utils'
import { useTranslation } from 'react-i18next'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { Card, CardHeader, CardText, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Row, Col, CardTitle } from 'reactstrap'

const ExternalVSInternal = ({ success }) => {
  const {t} = useTranslation()
  const [internal, setInternal] = useState({
    labels: [], // Add an empty array as the initial value
    total: 0,
    series: []
  })

  const [apiLoader, setApiLoader] = useState(false)
  const [checkApiData, setCheckApiData] = useState(true)
  const filterState = useSelector((store) => store.incident_charts)
  const apiLogic = () => {
    setApiLoader(true)
    axios
      .get(`/nids-incident-threat-type?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then((res) => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setInternal({
            labels: res.data.data.labels,
            total: res.data.data.total,
            series: res.data.data.series
          })
        }
      })
      .catch((error) => {
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
    labels: internal.labels,
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
              offsetY: 10,
              label: internal.total,
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
      <CardTitle className='mb-1'>{t('Type of Threat')}</CardTitle>
        <div style={{ height: '120px' }}>
        {checkApiData ? (
          <Row>
            <Col xs='6'>
            <div className='font-small-2'>{t('Total Threat Count')}</div>
              <h5 className='mb-1'>{internal.total}</h5>
            </Col>
            <Col xs='6'>
                <Chart options={options} series={internal.series} type='donut' height={120} />
            </Col>
          </Row>
          ) : (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
              <p>{t('Data Not Found')}</p>
            </div>
          )}
        </div>
      </CardBody>
      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default ExternalVSInternal
