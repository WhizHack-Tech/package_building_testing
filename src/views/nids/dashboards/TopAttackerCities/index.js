// ** Third Party Components
import Chart from 'react-apexcharts'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
import { Info } from 'react-feather'

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

    axios.get(`/nids-attck-event-city?condition=${filterState.values ? filterState.values : 'today'}`)
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

            colors: ['#ffe700', '#00d4bd', '#826bf8'],
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
                    show: true,
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
                      show: true,
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
      <CardHeader className='border-bottom'>
        <CardTitle>
          Top Attacked Cities
          {/* <span>
            <Button.Ripple className='btn-icon' color='flat-info' onClick={toggleCanvasScroll}>
              <Info size={16} />
            </Button.Ripple>
            <Offcanvas
              scrollable={canvasScroll}
              direction='end'
              isOpen={canvasOpen}
              toggle={toggleCanvasScroll}
            >
              <OffcanvasHeader toggle={toggleCanvasScroll} className='mt-2'>Critical Threats</OffcanvasHeader>
              <hr />
              <OffcanvasBody>
                <p>
                  Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web
                  designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have
                  scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book.
                </p>
              </OffcanvasBody>
            </Offcanvas>
          </span> */}
        </CardTitle>
        <Button.Ripple color='primary' outline size='sm' onClick={() => setModalBox(!modalBox)}>
          view More
        </Button.Ripple>

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
        {(chartData.series && chartData.series.length > 0) ? <Chart options={chartData.options} series={chartData.series} type='pie' height={350} /> : <DataNotFound />}
      </CardBody>

      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default PieCharts
