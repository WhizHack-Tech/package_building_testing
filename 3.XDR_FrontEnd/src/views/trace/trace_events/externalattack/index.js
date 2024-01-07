// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Events ( External Attacker Details )).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useEffect, useState } from 'react'
import axios from '@axios'
import Chart from 'react-apexcharts'
import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import PreLoader from '../../preLoader'
import { token } from '@utils'
import { useTranslation } from 'react-i18next'
import { Card, CardHeader, CardText, CardBody, Table, Button, Modal, ModalHeader, ModalBody, Label, Col, Input, Row } from 'reactstrap'
const ExternalAttackchart = ({ success }) => {
  const {t} = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [criticalThreatsTotal, setCriticalThreatsTotal] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart)
  const [checkApiData, setCheckApiData] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`/ext-trace-event?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setCriticalThreatsTotal(res.data)
          setTableData(res.data.filter)
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

  const filteredData = shortTableData.filter((rows) => rows.sensor_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
  rows.type_of_threat.toLowerCase().includes(searchQuery.toLowerCase())
)

  const options = {
    chart: {

      toolbar: {
        show: false
      },
      sparkline: {
        enabled: true
      }
    },
    grid: {
      show: true
    },
    colors: ['#00FFFF'],
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
        show: true
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
      data: criticalThreatsTotal.external_attack || [],
      name: 'External'
    }
  ]
  return (
    <Card>
      <div style={{ height: '230px' }}>
      <CardHeader className='align-items-start pb-0'>
        <div>
          <h2 className='font-weight-bolder'>{checkApiData ? criticalThreatsTotal.total : null}</h2>
          {/* <CardText>External Attack</CardText> */}
          <CardText>{t('External Attacks')}</CardText>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
          {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='xl'>
          <ModalHeader>{t('External Attacks')}</ModalHeader>
          <Row className='justify-content-end mx-0'>
            <Col className='d-flex align-items-center justify-content-end mt-1' md='6' sm='12'>
              <Label className='mr-1' for='search-input'>
                {t('Search')}
              </Label>
              <Input
                className='dataTable-filter mb-50'
                type='text'
                bsSize='sm'
                id='search-input'
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value.trim())}
              />
            </Col>
          </Row>
          <ModalBody>
            <Table striped responsive>
            <thead>
                <tr>
                  <th>{t('Sensor Name')}</th>
                  <th>{t('Lateral Movement')}</th>
                  <th>{t('Counts')}</th>
                  <th>{t('Actions')}</th>
                </tr>
              </thead>
              <tbody>
                {
                  (shortTableData.length === 0 || 
                    checkApiData === false ||
                    filteredData.length === 0
                    ) ? (
                    <tr>
                      <td colSpan={3} className='text-center'>{t('Data Not Found')}</td>
                    </tr>
                  ) : (
                    filteredData.map((rows, index) => {
                      return (
                        <tr key={index}>
                          <td>
                            <span className='align-middle fw-bold'>{rows.sensor_name}</span>
                          </td>
                          <td>
                            <span className='align-middle fw-bold'>{rows.type_of_threat}</span>
                          </td>
                          <td>
                            <span className='align-middle fw-bold'>{rows.threat_count}</span>
                          </td>
                          <td>
                            <Link to={`/trace-events-external-attack-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.sensor_name}`} className='btn-sm btn-outline-primary m-2'>
                              More Details
                            </Link>
                          </td>
                        </tr>
                      )
                    })
                  )
                }
              </tbody>
            </Table>
          </ModalBody>
        </Modal>
      </CardHeader>
      <CardBody>
        {checkApiData ? (
          <Chart options={options} series={series} type='area' height={200} />
        ) : (
          <p className='text-center' style={{ lineHeight: '230px' }}>{t('Data Not Found')}</p>
        )}
      </CardBody>
      </div>
      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default ExternalAttackchart
