// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Events ML & DL ( Attacker IP's)
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
import { token } from '@utils'
import { Info } from 'react-feather'
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Offcanvas, OffcanvasHeader, OffcanvasBody } from 'reactstrap'

import PreLoader from '../../preLoader'

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
            colors: ['#ffe700', '#00d4bd', '#826bf8', '#2b9bf4', '#FFA1A1', '#008000', '#f70d1a'],
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
          Source IPs
        </CardTitle>
        <div className='round overflow-hidden round overflow-hidden'>
                    <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
                        View More
                    </Button.Ripple>
                </div>
      </CardHeader>


      <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
        <ModalHeader>Source IPs</ModalHeader>
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
                        <Link to={`/nids-attacker-ips-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.name}`}>
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
