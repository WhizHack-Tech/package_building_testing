// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Alerts ( Attacker Target IP's Details ) ).
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

const targetIP = () => {
  const {t} = useTranslation()
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
  const [checkApiData, setCheckApiData] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const toggleCanvasScroll = () => {
    setCanvasScroll(true)
    setCanvasOpen(!canvasOpen)
  }


  const ChartApiLogic = () => {
    setApiLoader(true)

    axios.get(`/trace-alert-attker-ip-line?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
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

  const filteredData = shortTableData.filter((rows) => rows.sensor_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
  rows.attacker_ip.toLowerCase().includes(searchQuery.toLowerCase())
)

  return (
    <Card>
      <CardHeader className='border-bottom'>
        <CardTitle tag='h4'>
          {t('Source IPs')}
        </CardTitle>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            {t('View More')}
          </Button.Ripple>
        </div>
      </CardHeader>


      <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
        <ModalHeader>{t('Source IPs')}</ModalHeader>
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
                <th>{t('Source IPs')}</th>
                <th>{t('Counts')}</th>
                <th>{t('Actions')}</th>
              </tr>
            </thead>
            <tbody>
            {(
                  shortTableData.length === 0 ||
                  checkApiData === false ||
                  filteredData.length === 0
                ) ? (
                  <tr>
                    <td colSpan={4} className='text-center'>
                      {t('Data Not Found')}
                    </td>
                  </tr>
                ) : (
                  filteredData.map((rows, index) => {
                  return (
                    <tr key={index}>
                      <td>
                        <span className='align-middle fw-bold'>{rows.sensor_name}</span>
                      </td>
                      <td>
                        <span className='align-middle fw-bold'>{rows.attacker_ip}</span>
                      </td>
                      <td>
                        <span className='align-middle fw-bold'>{rows.attacker_ip_count}</span>
                      </td>
                      <td>
                        <Link to={`/trace-alert-attacker-ips-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.attacker_ip}&name1=${rows.sensor_name}`} className='btn-sm btn-outline-primary m-2'>
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
          <Chart options={chartData.options} series={chartData.series} type='line' height={450} />
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

export default targetIP
