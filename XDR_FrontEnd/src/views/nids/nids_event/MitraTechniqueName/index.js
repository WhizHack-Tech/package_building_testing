// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Events ( Mitre Technique Details )
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
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner, Offcanvas, OffcanvasHeader, OffcanvasBody } from 'reactstrap'

import PreLoader from '../preLoader'
import DataNotFound from '../dNotf'

const PieCharts = () => {

  const [chartData, setChartData] = useState({
    options: {},
    series: []
  })

  const [shortTableData, setTableData] = useState([])

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store => store.dashboard_chart))
  const [canvasOpen, setCanvasOpen] = useState(false)
  const [canvasScroll, setCanvasScroll] = useState(false)

  const toggleCanvasScroll = () => {
    setCanvasScroll(true)
    setCanvasOpen(!canvasOpen)
  }

  const ChartApiLogic = () => {
    setApiLoader(true)

    axios.get(`/nids-alert-mitre-techniq-bar-chart?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)
        if (res.data.message_type === "success") {

          // ** Chart Options
          const chartOption = {
            legend: {
              show: true,
              position: 'bottom'
            },
            labels: res.data.attacker_city.labels,
            colors: ['#EC6B56', '#FFC154', '#47B39C', '#826bf8', '#21409F', '#01a14b', '#3EB489', '#F70D1A', '#2916F5', '#F0E68C', '#EDDA74', '#FFD801', '#F4A460', '#C2B280', '#C04000', '#FF6347'],
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

          if (res.data.attacker_city.series.length > 0) {
            const tableDataRows = res.data.attacker_city.series.map((series, index) => ({
              series,
              labels: res.data.attacker_city.labels[index],
              past_time: res.data.filter.past_time,
              current_time: res.data.filter.current_time
            }))

            setTableData(tableDataRows)
          }


          // ** Chart Series
          setChartData({
            options: chartOption,
            series: res.data.attacker_city.series
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
  }, [filterState.values, filterState.refreshCount])

  return (
    <Card>
      <CardHeader>
        <CardTitle>
        Mitra Technique Name
        </CardTitle>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            View More
          </Button.Ripple>
        </div>

      </CardHeader>
      <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
        <ModalHeader>Top Attacked Countries</ModalHeader>
        <ModalBody>
          <Table striped responsive>
            <thead>
              <tr>
                <th>Countries</th>
                <th>Counts</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {
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
                        <Link to={`/top-attacked-city-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.labels}`}>
                          <Button.Ripple color='primary' outline size='sm'>
                            More Details
                          </Button.Ripple>
                        </Link>
                      </td>
                    </tr>
                  )
                })
              }
            </tbody>
          </Table>
        </ModalBody>
      </Modal>

      <CardBody>
        {(chartData.series && chartData.series.length > 0) ? <Chart options={chartData.options} series={chartData.series} type='pie' height={300} /> : <DataNotFound />}
      </CardBody>

      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default PieCharts