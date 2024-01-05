// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Incidents ( Top Source Attack Countries Details )).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { HorizontalBar } from 'react-chartjs-2'
import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardBody, Table, Button, Modal, ModalHeader, ModalBody, Label, Col, Input, Row } from 'reactstrap'
import axios from "@axios"
import { Link } from 'react-router-dom'
import { Info } from 'react-feather'
import { useSelector } from "react-redux"
import { useTranslation } from 'react-i18next'
import { token } from '@utils'
import PreLoader from '../../preLoader'
import DataNotFound from '../../dNotf'

const CountryChart = ({ tooltipShadow, gridLineColor, labelColor, successColorShade, lineChartPrimary, yellowColor }) => {
  const { t } = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [countriesTotal, setCountriesTotal] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart)
  const [checkApiData, setCheckApiData] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`/incident-attck-cntry-trace?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
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

  const filteredData = shortTableData.filter((rows) => rows.sensor_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
  rows.geoip_country_name.toLowerCase().includes(searchQuery.toLowerCase())
)

  const options = {
    elements: {
      rectangle: {
        borderWidth: 2,
        borderSkipped: 'bottom'
      }
    },
    responsive: true,
    maintainAspectRatio: false,
    responsiveAnimationDuration: 500,
    legend: {
      display: false
    },
    tooltips: {
      // Updated default tooltip UI
      shadowOffsetX: 1,
      shadowOffsetY: 1,
      shadowBlur: 8,
      shadowColor: tooltipShadow,
      backgroundColor: '#fff',
      titleFontColor: '#000',
      bodyFontColor: '#000'
    },
    scales: {
      xAxes: [
        {
          display: true,
          gridLines: {
            display: true,
            color: gridLineColor,
            zeroLineColor: gridLineColor
          },
          scaleLabel: {
            display: true,
            labelString: 'count'
          },
          ticks: {
            fontColor: labelColor
          }
        }
      ],
      yAxes: [
        {
          display: true,
          gridLines: {
            color: gridLineColor,
            zeroLineColor: gridLineColor
          },
          scaleLabel: {
            display: true,
            labelString: 'Countries'
          },
          ticks: {
            //stepSize: 1000,
            //  min: 0,
            // max: 400
            fontColor: labelColor
          }
        }
      ]
    }
  },
    data = {
      // labels: ['Routers', 'Laptops', 'Phones', 'Subnet', 'Servers', 'Dummy', 'Dummy'],
      labels: countriesTotal.labels,
      datasets: [
        {
          data: countriesTotal.series,
          backgroundColor: '#826bf8',
          borderColor: 'transparent',
          barThickness: 35
        }
      ]
    }
    

  return (
    <Card>
      <CardHeader className='d-flex justify-content-between align-items-sm-center align-items-start flex-sm-row flex-column'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Top Source Attack Countries')}
          </CardTitle>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
          {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='xl'>
          <ModalHeader>{t('Top Source Attack Countries')}</ModalHeader>
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
                  <th>{('Sensor Name')}</th>
                  <th>{t('Top Source Attack Countries')}</th>
                  <th>{t('Counts')}</th>
                  <th>{t('Actions')}</th>
                </tr>
              </thead>
              <tbody>
                {

                  (shortTableData.length === 0 || checkApiData === false || filteredData.length === 0) ? (
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
                            <span className='align-middle fw-bold'>{rows.geoip_country_name}</span>
                          </td>
                          <td>
                            <span className='align-middle fw-bold'>{rows.geoip_country_name_count}</span>
                          </td>
                          <td>
                            <Link to={`/trace-incident-countries-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.geoip_country_name}&name1=${rows.sensor_name}`} className='btn-sm btn-outline-primary m-2'>
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
            <HorizontalBar data={data} options={options} height={300} />
          ) : (
            <DataNotFound />
          )}
        </div>
      </CardBody>

      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default CountryChart
