// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Events ( Attacker Ports Details )).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Third Party Components
import Chart from 'react-apexcharts'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
import { Info } from 'react-feather'
import { token } from '@utils'
import { useTranslation } from 'react-i18next'
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, CardBody, Table, Button, Modal, ModalHeader, ModalBody, Label, Col, Input, Row } from 'reactstrap'

import PreLoader from '../../preLoader'
import DataNotFound from '../../dNotf'

const ApexRadiarChart = () => {
  const { t } = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [countriesTotal, setCountriesTotal] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart)
  const [checkApiData, setCheckApiData] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const toggleCanvasScroll = () => {
    setCanvasScroll(true)
    setCanvasOpen(!canvasOpen)
  }

  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`/attacker-port-trace-event?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setCountriesTotal(res.data.bar_chart)
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

  const filteredData = shortTableData.filter((rows) => rows.sensor_name.toLowerCase().includes(searchQuery.toLowerCase())
)

  // ** Chart Options
  const options = {
    legend: {
      show: true,
      position: 'bottom'
    },

    labels: countriesTotal ? countriesTotal.labels : [],

    colors: ['#826bf8', '#21409F', '#01a14b', '#3EB489', '#F70D1A', '#2916F5', '#F0E68C', '#EDDA74', '#FFD801', '#F4A460', '#C2B280', '#C04000', '#FF6347'],
    dataLabels: {
      enabled: true,
      formatter(val) {
        return `${parseInt(val)}%`
      }
    },
    plotOptions: {
      pie: {
        donut: {
          labels: {
            show: false,
            name: {
              fontSize: '1rem',
              fontFamily: 'Montserrat'
            },
            value: {
              fontSize: '1rem',
              fontFamily: 'Montserrat',
              formatter(val) {
                return `${parseInt(val)}%`
              }
            },
            total: {
              show: false,
              fontSize: '1.5rem',
              label: 'Operational',
              formatter() {
                return '31%'
              }
            }
          }
        }
      }
    },
    responsive: [
      {
        breakpoint: 992,
        options: {
          chart: {
            height: 380
          },
          legend: {
            position: 'bottom'
          }
        }
      },
      {
        breakpoint: 576,
        options: {
          chart: {
            height: 320
          },
          plotOptions: {
            pie: {
              donut: {
                labels: {
                  show: true,
                  name: {
                    fontSize: '1.5rem'
                  },
                  value: {
                    fontSize: '1rem'
                  },
                  total: {
                    fontSize: '1.5rem'
                  }
                }
              }
            }
          }
        }
      }
    ]
  }

  // ** Chart Series
  const series = countriesTotal ? countriesTotal.series : []

  return (
    <Card>
      <CardHeader className='d-flex justify-content-between align-items-sm-center align-items-start flex-sm-row flex-column'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Attacker Port')}
          </CardTitle>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
          <ModalHeader>{t('Attacker Port')}</ModalHeader>
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
                  <th>{t('Attacker Port')}</th>
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
                            <span className='align-middle fw-bold'>{rows.attacker_port}</span>
                          </td>
                          <td>
                            <span className='align-middle fw-bold'>{rows.attacker_port_count}</span>
                          </td>
                          <td>
                            <Link to={`/trace-events-attacker-port-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.attacker_port}&name1=${rows.sensor_name}`} className='btn-sm btn-outline-primary m-2'>
                              {t('More Details')}
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
        <div style={{ height: '350px' }}>
          {checkApiData ? (
            <Chart options={options} series={series} type='pie' height={350} />

          ) : (
            <DataNotFound />
          )}
        </div>
      </CardBody>
      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default ApexRadiarChart
