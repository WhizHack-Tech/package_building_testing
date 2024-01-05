// ** Third Party Components
import Chart from 'react-apexcharts'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
import { Info } from 'react-feather'
import { token } from '@utils'
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, CardBody, Table, Button, Modal, ModalHeader, ModalBody, Offcanvas, OffcanvasHeader, OffcanvasBody } from 'reactstrap'

import PreLoader from '../preLoader'

const LineCharts = () => {

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

    axios.get(`/nids-alert-attacker-ip-line-chart?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)
        if (res.data.message_type === "success") {

          // ** Chart Options
          const chartOption = {
            chart: {
              height: 300,
              type: 'line',
              zoom: {
                enabled: false
              },
              animations: {
                enabled: true
              }
            },
            stroke: {
              width: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              curve: 'straight'
            },
            labels: res.data.line_chart.labels,
            colors: ['#ffe700', '#00d4bd', '#826bf8'],
            xaxis: {
            }
          }

          if (res.data.filter.length > 0) {
            setTableData(res.data.filter)
          }

          // ** Chart Series
          setChartData({
            options: chartOption,
            series: res.data.line_chart.series
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
          Attacker IPs
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
              <OffcanvasHeader toggle={toggleCanvasScroll}>Line Charts</OffcanvasHeader>
              <hr />
              <OffcanvasBody>
                <p>
                  Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web
                  designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have
                  scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book.
                </p>
                <Button block color='primary' onClick={toggleCanvasScroll} className='mb-1'>
                  Continue
                </Button>
                <Button block outline color='secondary' onClick={toggleCanvasScroll}>
                  Cancel
                </Button>
              </OffcanvasBody>
            </Offcanvas>
          </span> */}
        </CardTitle>

        <Button.Ripple color='primary' outline size='sm' onClick={() => setModalBox(!modalBox)}>
          view More
        </Button.Ripple>

      </CardHeader>


      <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
        <ModalHeader>Attacker IPs</ModalHeader>
        <ModalBody>
          <Table striped responsive>
            <thead>
              <tr>
                <th>IPs</th>
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
                        <span className='align-middle fw-bold'>{rows.name}</span>
                      </td>
                      <td>
                        <span className='align-middle fw-bold'>{rows.count}</span>
                      </td>
                      <td>
                        <Link to={`/attacker-ips-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.name}`}>
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
        <Chart options={chartData.options} series={chartData.series} type='line' height={350} />
      </CardBody>

      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default LineCharts
