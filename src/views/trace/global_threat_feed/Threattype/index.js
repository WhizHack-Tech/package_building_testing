// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Golbal Threat Feed ( Threat Type Details ) ).
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
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner, Offcanvas, OffcanvasHeader, OffcanvasBody } from 'reactstrap'

import PreLoader from '../../preLoader'
import DataNotFound from '../../dNotf'

const CityChart = () => {
  const {t} = useTranslation()
  const [chartData, setChartData] = useState({
    options: {},
    series: []
  })
  const [shortTableData, setTableData] = useState([])

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store => store.global_charts))
  const [canvasOpen, setCanvasOpen] = useState(false)
  const [canvasScroll, setCanvasScroll] = useState(false)

  const [checkApiData, setCheckApiData] = useState(true)

  const toggleCanvasScroll = () => {
    setCanvasScroll(true)
    setCanvasOpen(!canvasOpen)
  }

  const ChartApiLogic = () => {
    setApiLoader(true)

    axios.get(`/glog-trace-threat-type-pie?condition=${filterState.values ? filterState.values : 'last_24_hours'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          
          const chartOption = {
            legend: {
              show: true,
              position: 'bottom'
            },
            labels: res.data.bar_chart.labels,
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
                      fontSize: '1.9rem',
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

          if (res.data.bar_chart.series.length > 0) {
            const tableDataRows = res.data.bar_chart.series.map((series, index) => ({
              series,
              labels: res.data.bar_chart.labels[index],
              past_time: res.data.filter.past_time,
              current_time: res.data.filter.current_time
            }))

            setTableData(tableDataRows)
          }


          // ** Chart Series
          setChartData({
            options: chartOption,
            series: res.data.bar_chart.series
          })


        }

      })
      .catch(error => {
        setApiLoader(false)
        console.log(error.message)
      })
  }

  useEffect(() => {
    ChartApiLogic()
  }, [filterState.filter_name, filterState.refreshCount])

  return (
    <Card>
      <CardHeader>
        <CardTitle>
        {t('Threat Type')}
        </CardTitle>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
          {t('View More')}
          </Button.Ripple>
        </div>
      </CardHeader>
      <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
        <ModalHeader>{t('Threat Type')}</ModalHeader>
        <ModalBody>
          <Table striped responsive>
            <thead>
              <tr>
                <th>{t('Threat Type')}</th>
                <th>{t('Counts')}</th>
                <th>{t('Actions')}</th>
              </tr>
            </thead>
            <tbody>
              {
                (shortTableData.length === 0 || checkApiData === false) ? (
                  <tr>
                    <td colSpan={3} className='text-center'>{t('Data Not Found')}</td>
                  </tr>
                ) : (
                  shortTableData.map((rows, index) => {
                    return (
                      <tr key={index}>
                        <td>
                          <span className='align-middle fw-bold'>{rows.labels}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.series}</span>
                        </td>
                        <td>
                          <Link to={`/trace-gobal-threat-type-source-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.labels}`} className='btn-sm btn-outline-primary m-2'>
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

      <CardBody>
        {checkApiData ? (
          <Chart options={chartData.options} series={chartData.series} type='pie' height={350} />
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

export default CityChart