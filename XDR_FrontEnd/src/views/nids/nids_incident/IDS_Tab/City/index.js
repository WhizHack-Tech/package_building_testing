// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Incidents IDS ( Attacker City )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Third Party Components
import Chart from 'react-apexcharts'
import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardBody, Table, Button, Modal, ModalHeader, ModalBody } from 'reactstrap'
import axios from "@axios"
import { Link } from 'react-router-dom'
import { useSelector } from "react-redux"
import { useTranslation } from 'react-i18next'
import { token } from '@utils'
import PreLoader from '../../preLoader'

const ApexRadiarChart = () => {

  const { t } = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [criticalThreatsTotal, setCriticalThreatsTotal] = useState([])

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.incident_charts)
  const [checkApiData, setCheckApiData] = useState(true)

  const apiLogic = () => {
    setApiLoader(true)
    axios.get(`/nids-incident-city-pie-chart?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setCriticalThreatsTotal(res.data.pie_chart)
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

  const options = {
    legend: {
      show: true,
      position: 'bottom'
    },
    labels: criticalThreatsTotal.labels || [],

    colors: ['#826bf8', '#21409F', '#01a14b', '#3EB489', '#F70D1A', '#2916F5', '#F0E68C', '#EDDA74', '#FFD801', '#F4A460', '#C2B280', '#C04000', '#FF6347'],
    dataLabels: {
      enabled: true,
      formatter(val, opt) {
        return `${parseInt(val)}%`
      }
    },
    plotOptions: {
      pie: {
        donut: {
          labels: {
            show: false,
            name: {
              fontSize: '2rem',
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
              formatter(w) {
                return '31'
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

  const series = criticalThreatsTotal.series?.length > 0 ? criticalThreatsTotal.series : []

  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Top Attacker City')}
          </CardTitle>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
          <ModalHeader>{t('Top Attacker City')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Top Attacker City')}</th>
                  <th>{t('Platform')}</th>
                  <th>{t('Counts')}</th>
                  <th>{t('Actions')}</th>
                </tr>
              </thead>
              <tbody>
                {(shortTableData.length === 0 || checkApiData === false) ? (
                <tr>
                  <td colSpan={7} className='text-center'>{t('Data Not Found')}</td>
                </tr>
              ) : (
                  shortTableData.map((rows, index) => {
                    return (
                      <tr key={index}>
                        <td>
                          <span className='align-middle fw-bold'>{rows.geoip_city}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.platform}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.geoip_city_count}</span>
                        </td>
                        <td>
                          <Link to={`/nids-incident-ids-city-details?current_time=${rows.current_time}&past_time=${rows.past_time}&geoip_city=${rows.geoip_city}&platform=${rows.platform}`} className='btn-sm btn-outline-primary m-2'>
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
        {checkApiData ? (
          <Chart options={options} series={series} type='pie' height={350} />
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <p>{t('Data Not Found')}</p>
          </div>
        )}
      </CardBody>
      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default ApexRadiarChart